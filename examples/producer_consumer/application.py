from fastflow import FastFlow

app = FastFlow()
wf = app.workflow("producer-consumer")


@wf.input()
async def produce_records(val: str) -> int:
    return int(val)


@wf.input()
async def consumer_offset(val: str) -> int:
    return int(val)


@wf.task()
async def start() -> None:
    print("[task] in start")


@wf.producer("records", after=[start])
async def produce(
    # records: int = Input(produce_records),
) -> str:
    return "[producer] in produce"


# @wf.consumer("records", offset=consumer_offset)
@wf.consumer("records")
async def consume() -> str:
    return "[consumer] in consume"


@wf.task(after=[consume])
async def finish() -> None:
    print("[task] in finish")


async def main(
    produce_records: str,
    consumer_offset: str,
):
    print(f"//{('*' * 50)}")
    print("// WORKFLOW NAME")
    print(f"//{('*' * 50)}")
    print(wf.name)
    print("")

    print(f"//{('*' * 50)}")
    print("// INPUTS")
    print(f"//{('*' * 50)}")
    print(wf.inputs)
    for input in wf._inputs:
        if input.__name__ == "produce_records":
            print(await input(produce_records))
        elif input.__name__ == "consumer_offset":
            print(await input(consumer_offset))
        else:
            raise ValueError("unhandled input")
            
    print("")

    print(f"//{('*' * 50)}")
    print("// ACTIVITIES")
    print(f"//{('*' * 50)}")
    # print(wf.activities)
    for activity in wf._activities:
        print(f"--- {activity}")
        print(await activity())


import asyncio

asyncio.run(
    main(
        produce_records="10",
        consumer_offset="5",
    )
)
