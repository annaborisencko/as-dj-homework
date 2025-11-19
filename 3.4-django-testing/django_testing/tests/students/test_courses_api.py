import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Course, Student 

@pytest.fixture
def client():
    """Фикстура для клиента API"""
    return APIClient()

@pytest.fixture
def student_factory():
    """Фабрика студентов"""
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory

@pytest.fixture
def course_factory():
    """Фабрика курсов"""
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

@pytest.fixture
def course_with_students_factory(student_factory, course_factory, student_count=1, course_count=1):
    """Фабрика курсов"""
    def factory(*args, **kwargs):
        students = student_factory(_quantity=student_count)
        courses = course_factory(_quantity=course_count, students=students)
        return courses
    return factory

@pytest.mark.django_db
def test_add_course(client, student_factory):
    """Тест успешного создания курса"""
    course_count = Course.objects.count()
    students = student_factory(_quantity=5)
    data = {
        'name': 'Русский язык',
        'students': [student.id for student in students]
    }
    response = client.post('/api/v1/courses/', data)

    # Проверим, что вернулся статус 201
    assert response.status_code == 201, f'Ошибка создания курса, сервер вернул статус {response.status_code} вместо 201'
    # Проверим, что в результате запроса в БД была создана 1 запись 
    assert Course.objects.count() == course_count+1, f'Ошибка создания курса, число курсов в БД до создания {course_count}, после - {Course.objects.count()}'

@pytest.mark.django_db
def test_update_course(client, course_with_students_factory):
    """Тест успешного обновления курса"""
    add_course = course_with_students_factory()
    course = Course.objects.all().first()
    course_count = Course.objects.count()
    data = {
        'name': 'Английский язык',
    }
    url = f'/api/v1/courses/'+str(course.id)+f'/'
    response = client.put(url, data)

    # Проверим, что вернулся статус 200
    assert response.status_code == 200, f'Ошибка изменения курса, сервер вернул статус {response.status_code} вместо 200'
    # Проверим, что новое наименование курса совпадает с переданным значением 
    assert Course.objects.get(id=course.id).name == data['name'], f'Ошибка изменения курса, наименование курса после изменения {Course.objects.get(id=course.id).name}, вместо - {data['name']}'
     # Проверим, что в результате запроса запись в БД была обновлена, а не добавлена
    assert Course.objects.count() == course_count, f'Ошибка изменения курса. Число записей в БД до {course_count} и после {Course.objects.count()} операции не совпадают.'

@pytest.mark.django_db
def test_delete_course(client, course_with_students_factory):
    """Тест успешного удаления курса"""
    courses = course_with_students_factory(course_count=5)
    course_count = Course.objects.count()
    course = Course.objects.all().first()
    url = f'/api/v1/courses/'+str(course.id)+f'/'
    response = client.delete(url)

    # Проверим, что вернулся статус 204
    assert response.status_code == 204, f'Ошибка удаления курса, сервер вернул статус {response.status_code} вместо 204'
    # Проверим, что число записей в БД уменьшилось на 1 после запроса 
    assert Course.objects.count() == course_count-1, f'Ошибка создания курса, число курсов в БД до создания {course_count}, после - {Course.objects.count()}'

@pytest.mark.django_db
def test_get_first_course(client, course_with_students_factory):
    """Тест успешного получения первого курса"""
    courses = course_with_students_factory(course_count=5)
    course = Course.objects.all().first()
    url = f'/api/v1/courses/'+str(course.id)+f'/'
    response = client.get(url)

    # Проверим, что вернулся статус 200
    assert response.status_code == 200, f"Ошибка получения данных первого курса, сервер вернул статус {response.status_code} вместо 200"
    response_json = response.json()
    # Проверим, что идентификатор полученного курса и курса в БД совпадают
    assert  response_json.get('id') == course.id, f"Ошибка получения данных первого курса, данные курса в БД - {course.id}, получено - {response_json.get('id')}"

@pytest.mark.django_db
def test_get_course_list(client, course_with_students_factory):
    """Тест успешного получения списка курсов"""
    courses = course_with_students_factory(course_count=5)
    course_count = Course.objects.count()
    url = f'/api/v1/courses/'
    response = client.get(url)

    # Проверим, что вернулся статус 200 
    assert response.status_code == 200, f"Ошибка получения списка курсов, сервер вернул статус {response.status_code} вместо 200"
    response_json = response.json()
    # Проверим, что количество записей в полученном списке совпадает с количеством записей в БД 
    assert len(response_json) == course_count, f"Ошибка получения списка курсов, число курсов в БД - {course_count}, получено - {len(response_json)}"
    # Проверим, что значение в поле "name" для первоой записи в БД и первой записи в ответе совпадают
    assert response_json[0]['name'] == Course.objects.all().first().name, f"Ошибка получения данных первого курса, данные курса в БД - {Course.objects.all().first().name}, получено - {response_json[0]['name']}"

@pytest.mark.django_db
def test_get_course_list_filter_by_id(client, course_with_students_factory):
    """Тест успешного получения курса с филтром"""
    courses = course_with_students_factory(course_count=5)
    course = Course.objects.all().last()
    url = f'/api/v1/courses/?id='+str(course.id)
    response = client.get(url)

    # Проверим, что вернулся статус 200 
    assert response.status_code == 200, f"Ошибка получения курса по его идентификатору, сервер вернул статус {response.status_code} вместо 200"
    response_json = response.json()
    # Проверим, что значение в поле "name" для записи в БД и в ответе совпадают
    assert response_json[0]['name'] == course.name, f"Ошибка получения данных первого курса, данные курса в БД - {course.name}, получено - {response_json[0]['name']}"

@pytest.mark.django_db
def test_get_course_list_filter_by_name(client, course_with_students_factory):
    """Тест успешного получения курса с филтром"""
    courses = course_with_students_factory(course_count=5)
    course = Course.objects.all().last()
    url = f'/api/v1/courses/?name='+str(course.name)
    response = client.get(url)

    # Проверим, что вернулся статус 200 
    assert response.status_code == 200, f"Ошибка получения курса по его наименованию, сервер вернул статус {response.status_code} вместо 200"
    response_json = response.json()
    # Проверим, что значение в поле "id" для записи в БД и в ответе совпадают
    assert response_json[0]['id'] == course.id, f"Ошибка получения данных первого курса, данные курса в БД - {course.id}, получено - {response_json[0]['id']}"


@pytest.mark.parametrize('max_students,student_count', [
    (2, 3),
    (2, 2),
    (2, 1), 
])
@pytest.mark.django_db
def test_add_max_students(client, settings, max_students, student_count, student_factory):
    settings.MAX_STUDENTS_PER_COURSE = max_students
    students = student_factory(_quantity=student_count)
    data = {
        'name': 'Название курса',
        'students': [student.id for student in students]
    }
    url = "/api/v1/courses/"
    response = client.post(url, data)
    # Проверим, что вернулся статус 201 
    assert response.status_code == 201, f"Курс не создан, допустимое число студентов на курсе - {max_students}, а передано {student_count}."

@pytest.mark.parametrize('max_students,student_count', [
    (2, 3),
    (2, 2),
    (2, 1), 
])
@pytest.mark.django_db
def test_put_max_students(client, settings, max_students, student_count, student_factory, course_with_students_factory):
    settings.MAX_STUDENTS_PER_COURSE = max_students
    courses = course_with_students_factory(student_count=max_students)
    course = Course.objects.all().first()
    students = student_factory(_quantity=student_count)
    data = {
        'name': course.name,
        'students': [student.id for student in students]
    }
    url = f'/api/v1/courses/'+str(course.id)+f'/'
    response = client.put(url, data)
    # Проверим, что вернулся статус 200
    assert response.status_code == 200, f"Курс не изменен, допустимое число студентов на курсе - {max_students}, а передано {student_count}."
   