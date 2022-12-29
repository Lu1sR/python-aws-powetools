from typing import Dict, Optional
from aws_lambda_powertools.event_handler.api_gateway import Router
from sqlmodel import  Session, select
from src.models.hero import Hero
import boto3, json



#https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
#TODO mock test and debug dynamodb connection

router = Router()

# tableName = 'tickets'
# dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
# db = dynamodb.Table(tableName)


@router.get("/hero")
def get_users():
    # allUsers = db.scan()
    # return {"tickets": allUsers}
    engine = router.context.get("engine")
    with Session(engine) as session:
        statement = select(Hero)
        results = session.exec(statement)
        heroes = results.all()
        print(heroes)
        return [hero.dict() for hero in heroes]


@router.get("/hero/<key>")
def get_users(key: str):
    # response = db.get_item(
    #     Key={
    #         'id': key
    #     }
    # )
    # item = response['Item']
    # return {"tickets": item }
    engine = router.context.get("engine")
    with Session(engine) as session:
        statement = select(Hero).where(Hero.id == key)
        result = session.exec(statement)
        hero = result.first()
        print(hero)
        return hero.dict()


@router.post("/hero")
def create_hero():
    engine  = router.context.get("engine")
    raw_data: Optional[str] = router.current_event.body  # raw str | None
    data: Dict = json.loads(raw_data)
    hero_1 = Hero(name=data['name'], secret_name=data['secret_name'], age=48)
    with Session(engine) as session:
        session.add(hero_1)
        session.commit()
        return {"result": "ok"}


@router.put("/hero")
def update_hero():
    engine  = router.context.get("engine")
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        results = session.exec(statement)
        hero_1 = results.one() # will raise an exception if there are no objects in results
        print("Hero 1:", hero_1)

        hero_1.age = 16
        hero_1.name = "Spider-Youngster"
        session.add(hero_1)

        session.commit()
        session.refresh(hero_1)
        print("Updated hero 1:", hero_1)
        return [hero_1.dict()]


@router.delete("/hero")
def update_hero():
    engine  = router.context.get("engine")
    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Youngster")  
        results = session.exec(statement)  
        hero = results.one()  
        print("Hero: ", hero)  

        session.delete(hero)  
        session.commit()  

        print("Deleted hero:", hero)  
        return {"deleted_id": hero.id}