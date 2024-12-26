import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Student, Course


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def course_factory():
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory


@pytest.fixture
def student_factory():
    def factory(*args, **kwargs):
        return baker.make(Student, *args, **kwargs)
    return factory



# проверка получения первого курса (retrieve-логика):
# создаем курс через фабрику;
# строим урл и делаем запрос через тестовый клиент;
# проверяем, что вернулся именно тот курс, который запрашивали

@pytest.mark.django_db
def test_get_course(api_client, course_factory):

    course = course_factory()

    response = api_client.get(f"/api/v1/courses/{course.id}/")

    assert response.status_code == 200
    data = response.json()
    assert course.name == data["name"]
    assert course.id == data["id"]


# проверка получения списка курсов (list-логика)
# аналогично — сначала вызываем фабрики, затем делаем запрос и проверяем результат

@pytest.mark.django_db
def test_get_courses_list(api_client, course_factory):

    courses = course_factory(_quantity=5)

    response = api_client.get("/api/v1/courses/")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == len(courses)
    for index, course in enumerate(data):
        assert course["name"] == courses[index].name


# проверка фильтрации списка курсов по id
# создаем курсы через фабрику, передать ID одного курса в фильтр, проверить результат запроса с фильтром

@pytest.mark.django_db
def test_get_course_filter_by_id(api_client, course_factory):

    courses = course_factory(_quantity=5)
    course_id = courses[0].id

    response = api_client.get(f"/api/v1/courses/?id={course_id}")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == course_id


# проверка фильтрации списка курсов по name

@pytest.mark.django_db
def test_get_course_filter_by_name(api_client, course_factory):

    courses = course_factory(_quantity=5)
    course_name = courses[0].name
    
    response = api_client.get(f"/api/v1/courses/?name={course_name}")

    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == course_name


# тест успешного создания курса
# здесь фабрика не нужна, готовим JSON-данные и создаём курс

@pytest.mark.django_db
def test_create_course(api_client):

    count_of_courses = Course.objects.count()
    student = Student.objects.create(name="Ivan", birth_date="2000-01-01")
    data = {"name": "Python", "students": [student.id]}

    response = api_client.post("/api/v1/courses/", data=data)

    assert response.status_code == 201
    assert Course.objects.count() == count_of_courses + 1


# тест успешного обновления курса
# сначала через фабрику создаём, потом обновляем JSON-данными

@pytest.mark.django_db
def test_update_course(api_client, course_factory, student_factory):

    course = course_factory()
    new_name = "Python"
    students = student_factory(_quantity=5)
    data = {"name": new_name, "students": [student.id for student in students]}

    response = api_client.patch(f"/api/v1/courses/{course.id}/", data=data)

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == new_name
    assert len(data["students"]) == 5
    for index, student_id in enumerate(data["students"]):
        assert student_id == students[index].id

    

# тест успешного удаления курса

@pytest.mark.django_db
def test_delete_course(api_client, course_factory):

    courses = course_factory(_quantity=1)
    
    response = api_client.delete(f"/api/v1/courses/{courses[0].id}/")
    response1 = api_client.get("/api/v1/courses/")

    assert response.status_code == 204
    data = response1.json()
    assert len(data) == 0

