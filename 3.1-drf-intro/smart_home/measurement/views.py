# TODO: опишите необходимые обработчики, рекомендуется использовать generics APIView классы:
# TODO: ListCreateAPIView, RetrieveUpdateAPIView, CreateAPIView
from .serializers import SensorSerializer, MeasurementSerializer, SensorListSerializer
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .models import Sensor, Measurement
from rest_framework.response import Response

class SensorListView(ListAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorListSerializer

    def post(self, request):
        new_sensor = Sensor.objects.create(
            name=request.data.get('name'),
            description=request.data.get('description')
        )
        if new_sensor.id:
            serializer = self.get_serializer(new_sensor)
            return Response(serializer.data)

        return Response(new_sensor)

class SensorView(RetrieveAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer

    def patch(self, request, pk):
        updated_sensor_count = Sensor.objects.filter(id=pk).update(
            name=request.data.get('name'),
            description=request.data.get('description')
        )
        if updated_sensor_count == 1:
            updated_sensor = Sensor.objects.get(id=pk)
            serializer = self.get_serializer(updated_sensor)
    
            return Response(serializer.data)
        else:
            return f"Не удалось обновить данные"


    def delete(self, request, pk):
        deleted_sensor_count = Sensor.objects.filter(id=pk).delete()
        if deleted_sensor_count[0] == 1:    
            return Response({'message': f"Данные успешно удалены"})
        else:
            return Response({'error': f"Не удалось удалить данные"})   

class MeasurementView(RetrieveAPIView):
    queryset = Measurement.objects.all()
    serializer_class = MeasurementSerializer

    def post(self, request):
        new_measure = Measurement.objects.create(
            sensor = Sensor.objects.get(id=request.data.get('sensor')),
            temperature=request.data.get('temperature')
        )
        if new_measure.id:
            serializer = self.get_serializer(new_measure)
            return Response(serializer.data)

        return Response(new_measure)