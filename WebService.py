from flask import Flask
from flask_graphql import GraphQLView
from graphene import ObjectType, String, Schema, Float, Field, Mutation, InputObjectType, List
from datetime import datetime


class SensorData(ObjectType):
    id = String()
    temperature = Float()
    humidity = Float()
    light = Float()
    timestamp = String()


class SensorDataInput(InputObjectType):
    temperature = Float(required=True)
    humidity = Float(required=True)
    light = Float(required=True)


class UpdateSensorData(Mutation):
    class Arguments:
        id = String(required=True)
        input = SensorDataInput(required=True)

    sensor_data = Field(lambda: SensorData)

    def mutate(root, info, id, input):
        if id in sensor_data_dict:
            sensor_data_dict[id] = {
                'id': id,
                'temperature': input.temperature,
                'humidity': input.humidity,
                'light': input.light,
                'timestamp': datetime.now().isoformat(timespec='seconds')
            }
            return UpdateSensorData(sensor_data=sensor_data_dict[id])
        else:
            raise Exception("O ID requisitado não existe.")

# Mutação GraphQl para atualizar um registro
'''
mutation {
  updateSensorData(id: "<ID DO REGISTRO>", input: {temperature: 24.5, humidity: 46.6, light: 79.9}) {
    sensorData {
      id
      temperature
      humidity
      light
      timestamp
    }
  }
}
'''

class DeleteSensorData(Mutation):
    class Arguments:
        id = String(required=True)

    ok = String()

    def mutate(root, info, id):
        if id in sensor_data_dict:
            del sensor_data_dict[id]
            return DeleteSensorData(ok="Informações deletadas com sucesso!")
        else:
            raise Exception("O ID requisitado não existe.")


next_id = 1
sensor_data_dict = {}

# Mutação GraphQl para deletar um registro
'''
mutation {
  deleteSensorData(id: "<ID DO REGISTRO>") {
    ok
  }
}
'''

class CreateSensorData(Mutation):
    class Arguments:
        input = SensorDataInput(required=True)

    sensor_data = Field(lambda: SensorData)

    def mutate(root, info, input):
        global next_id
        id = str(next_id)
        sensor_data_dict[id] = {
            'id': id,
            'temperature': input.temperature,
            'humidity': input.humidity,
            'light': input.light,
            'timestamp': datetime.now().isoformat(timespec='seconds')
        }
        next_id += 1
        return CreateSensorData(sensor_data=sensor_data_dict[id])

# Mutação GraphQL para criar um novo registro
'''
mutation {
  createSensorData(input: {temperature: 23.5, humidity: 45.6, light: 78.9}) {
    sensorData {
      id
      temperature
      humidity
      light
      timestamp
    }
  }
}
'''

class Query(ObjectType):
    sensor_data = Field(SensorData, id=String(required=True))
    sensor_data_by_time = Field(SensorData, timestamp=String(required=True))
    all_sensor_data = List(SensorData)
    last_id = String()

    def resolve_sensor_data(root, info, id):
        if id in sensor_data_dict:
            return sensor_data_dict.get(id)
        else:
            raise Exception("O ID requisitado não existe.")

    def resolve_sensor_data_by_time(root, info, timestamp):
        for data in sensor_data_dict.values():
            if data['timestamp'] == timestamp:
                return data

    def resolve_last_id(root, info):
        return str(next_id - 1)

    def resolve_all_sensor_data(root, info):
        return sensor_data_dict.values()

# Consulta GraphQL para obter a lista de todos os registros
'''
{
  allSensorData {
    id
    temperature
    humidity
    light
    timestamp
  }
}
'''
class Mutation(ObjectType):
    create_sensor_data = CreateSensorData.Field()
    update_sensor_data = UpdateSensorData.Field()
    delete_sensor_data = DeleteSensorData.Field()


schema = Schema(query=Query, mutation=Mutation)

app = Flask(__name__)
app.add_url_rule(
    '/graphql', view_func=GraphQLView.as_view('graphql', schema=schema, graphiql=True))

if __name__ == '__main__':
    app.run()
