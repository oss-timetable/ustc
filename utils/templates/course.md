# {{semester.name}} {{course.name}} {{course.teacherName}}


{% if course.exams | length > 0 %}

## 考试安排

| 考试名称 | 考试时间 | 考试地点 | 考试类型 | 考试模式 |
| -------- | -------- | -------- | -------- | -------- |
{% for exam in course.exams %}| {{exam.name}} | {{exam.startDate | unix_timestamp_to_date_str }} - {{exam.endDate | unix_timestamp_to_date_str("%H:%M") }} | {{exam.location}} | {{exam.examType}} | {{exam.examMode}} |
{% endfor %}
{% endif %}

{% if course.homeworks | length > 0 %}
## 作业情况
{% for homework in course.homeworks | sort(attribute='index', reverse = True) %}
### {{homework.name}}

{% if homework.deadline %}
- 截止时间：{{homework.deadline | unix_timestamp_to_date_str("%Y-%m-%d %H:%M") }}
{% endif %}

- 作业内容：

{{homework.content}}
{% endfor %}
{% endif %}

## 课程信息

- 课程号：{{course.lessonCode}}
- 学分：{{course.credit}}
- 教学类型：{{course.courseType}}
- 开课单位：{{course.openDepartment}}
- 课程类别：{{course.courseGradation}}
- 课程层次：{{course.courseCategory}}

## 上课时间

```
{{course.dateTimePlacePersonText}}
```

{% if course.description | length > 0 %}

## 课程简介

{{course.description}}

{% endif %}
