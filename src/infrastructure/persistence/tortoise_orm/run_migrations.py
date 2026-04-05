from tortoise import Tortoise, run_async


async def init():
    # Here we connect to a SQLite DB file.
    # also specify the app name of "models"
    # which contain models from "app.models"
    await Tortoise.init(
        db_url="sqlite://db.sqlite3", modules={"models": ["app.models"]}
    )
    # Generate the schema
    await Tortoise.generate_schemas()


run_async(init())
