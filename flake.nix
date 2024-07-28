{
  description = "Fastflow. In process streaming workflow engine";

  inputs = {
    dream2nix.url = "github:nix-community/dream2nix";
    nixpkgs.follows = "dream2nix/nixpkgs";
  };

  outputs = {
    self,
    dream2nix,
    nixpkgs,
    ...
  }: let
    supportedSystems = ["x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin"];
    forEachSupportedSystem = f:
      nixpkgs.lib.genAttrs supportedSystems (supportedSystem:
        f rec {
          system = supportedSystem;
          pkgs = import nixpkgs {
            inherit system;
            overlays = [ ];
          };
          db2Driver =
            if pkgs.stdenv.isLinux
            then "${pkgs.odbc-driver-pkgs.db2-odbc-driver}/lib/libdb2o.so"
            else "${pkgs.odbc-driver-pkgs.db2-odbc-driver}/lib/libdb2o.dylib";
        });
  in {
    packages = forEachSupportedSystem ({pkgs, ...}: rec {
      prod = dream2nix.lib.evalModules {
        packageSets.nixpkgs = pkgs;
        modules = [
          ./default.nix
          {
            paths.projectRoot = ./.;
            paths.projectRootFile = "flake.nix";
            paths.package = ./.;
            paths.lockFile =
              if pkgs.stdenv.isDarwin
              then "lock.prod.darwin.json"
              else "lock.prod.linux.json";
          }
        ];
      };
      dev = dream2nix.lib.evalModules {
        packageSets.nixpkgs = pkgs;
        modules = [
          ./default.nix
          {
            paths.projectRoot = ./.;
            paths.projectRootFile = "flake.nix";
            paths.package = ./.;
            paths.lockFile =
              if pkgs.stdenv.isDarwin
              then "lock.dev.darwin.json"
              else "lock.dev.linux.json";
            flags.groupDev = true;
          }
        ];
      };
      default = prod;
    });

    # nix fmt
    formatter = forEachSupportedSystem ({pkgs, ...}: pkgs.alejandra);

    # nix develop
    devShells = forEachSupportedSystem ({
      system,
      pkgs,
      ...
    }: {
      # nix develop -c $SHELL
      default = pkgs.mkShell {
        inputsFrom = [
          self.packages.${system}.dev.devShell
        ];

        packages = with pkgs;
          [
            argc
          ];

        shellHook = ''
          export IN_NIX_DEVSHELL=1;
        '';
      };
    });

    overlay = final: prev: {
      fastflow = self.packages.${prev.system};
    };
  };
}
