from fastapi import FastAPI, Query, Path, HTTPException
from course import Course

app = FastAPI()

courses = [
    Course(id=1, title="Python Basics", description="Python course for beginners"),
    Course(id=2, title="Python Advanced", description="Python advance course for developers"),
    Course(id=3, title="Javascript", description="Javascript course from zero to hero"),
    Course(id=4, title="React", description="Learn React with this fun course")
]


@app.get("/", summary="Get all courses", description="Get all available courses in the list",
         response_model=list[Course], name="get_all")
def get_courses():
    return courses


@app.get("/{course_id}", name="get_course_by_id"
    , summary="search course by id",
         description="search course by id, a course will be returned if found or 404 error for invalid id",
         response_model=Course)
def get_course_by_id(course_id: int = Path(description="unique id of the course")):
    course_found = next(filter(lambda course: course.id == course_id, courses), None)
    if course_found:
        return course_found
    raise HTTPException(status_code=404, detail=f"No course found with course id {course_id}")


@app.get("/courses/", name="get_course_by_title"
    , summary="search courses by title",
         description="search courses by title either part or full title", response_model=list[Course])
def get_courses_by_name(title: str = Query(description="Enter part of the course")):
    return [course for course in courses if course.title.find(title) != -1]


@app.post("/create", name="create_course"
    , summary="Create a new course",
          description="Create a new course by passing relevant details",
          response_model=Course)
def create_course(course: Course):
    max_id = max(courses, key=lambda cur_course: cur_course.id).id
    max_id += 1

    course.id = max_id
    courses.append(course)
    return course


@app.put("/update/{course_id}", name="update_course"
    , summary="update a course details",
         description="update course by passing new course details and existing course id",
         response_model=Course)
def update_course(course_id: int, course: Course):
    course_to_update = next(filter(lambda cur_course: cur_course.id == course_id, courses))
    if course_to_update:
        course_to_update.title = course.title
        course_to_update.description = course.description
        return course_to_update
    else:
        raise HTTPException(status_code=404, detail=f"No course found with course id {course_id}")



@app.delete("/delete", name="delete_course"
    , summary="delete course by id",
            description="delete course by id, a course will be returned if found or 404 error for invalid id",
            response_model=Course)
def delete_course(course_id: int):
    course_to_delete = next(filter(lambda cur_course: cur_course.id == course_id, courses))
    if course_to_delete:
        courses[:] = [course for course in courses if course.id != course_id]
    else:
        raise HTTPException(status_code=404, detail=f"No course found with course id {course_id}")
