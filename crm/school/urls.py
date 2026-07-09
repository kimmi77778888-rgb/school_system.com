from django.urls import path
from . import views

app_name = 'school'

urlpatterns = [
    # Auth
    path('login/',    views.login_view,        name='login'),
    path('logout/',   views.logout_view,       name='logout'),
    path('profile/',  views.profile_update,    name='profile_update'),
    path('settings/', views.school_settings_view, name='school_settings'),

    # Dashboard
    path('', views.dashboard, name='dashboard'),

    # Users
    path('users/',              views.user_list,   name='user_list'),
    path('users/add/',          views.user_add,    name='user_add'),
    path('users/<int:pk>/delete/', views.user_delete, name='user_delete'),

    # Students
    path('students/',                   views.student_list,   name='student_list'),
    path('students/add/',               views.student_add,    name='student_add'),
    path('students/<int:pk>/',          views.student_detail, name='student_detail'),
    path('students/<int:pk>/edit/',     views.student_edit,   name='student_edit'),
    path('students/<int:pk>/delete/',   views.student_delete, name='student_delete'),

    # Teachers
    path('teachers/',                   views.teacher_list,   name='teacher_list'),
    path('teachers/add/',               views.teacher_add,    name='teacher_add'),
    path('teachers/<int:pk>/',          views.teacher_detail, name='teacher_detail'),
    path('teachers/<int:pk>/edit/',     views.teacher_edit,   name='teacher_edit'),
    path('teachers/<int:pk>/delete/',   views.teacher_delete, name='teacher_delete'),

    # Academic Years
    path('academic-years/',                     views.academic_year_list,       name='academic_year_list'),
    path('academic-years/add/',                 views.academic_year_add,        name='academic_year_add'),
    path('academic-years/generate/',            views.academic_year_generate,   name='academic_year_generate'),
    path('academic-years/<int:pk>/edit/',       views.academic_year_edit,       name='academic_year_edit'),
    path('academic-years/<int:pk>/delete/',     views.academic_year_delete,     name='academic_year_delete'),
    path('academic-years/<int:pk>/set-active/', views.academic_year_set_active, name='academic_year_set_active'),

    # Classrooms
    path('classrooms/',                 views.classroom_list,   name='classroom_list'),
    path('classrooms/add/',             views.classroom_add,    name='classroom_add'),
    path('classrooms/<int:pk>/edit/',   views.classroom_edit,   name='classroom_edit'),
    path('classrooms/<int:pk>/delete/', views.classroom_delete, name='classroom_delete'),

    # Subjects
    path('subjects/',                   views.subject_list,   name='subject_list'),
    path('subjects/add/',               views.subject_add,    name='subject_add'),
    path('subjects/<int:pk>/edit/',     views.subject_edit,   name='subject_edit'),
    path('subjects/<int:pk>/delete/',   views.subject_delete, name='subject_delete'),

    # Attendance
    path('attendance/',         views.attendance_list, name='attendance_list'),
    path('attendance/add/',     views.attendance_add,  name='attendance_add'),
    path('attendance/bulk/',    views.attendance_bulk, name='attendance_bulk'),

    # Teacher Attendance
    path('teacher-attendance/',        views.teacher_attendance_list,  name='teacher_attendance_list'),
    path('teacher-attendance/add/',    views.teacher_attendance_add,   name='teacher_attendance_add'),
    path('teacher-attendance/bulk/',   views.teacher_attendance_bulk,  name='teacher_attendance_bulk'),

    # Exams
    path('exams/',                  views.exam_list,   name='exam_list'),
    path('exams/add/',              views.exam_add,    name='exam_add'),
    path('exams/<int:pk>/edit/',    views.exam_edit,   name='exam_edit'),
    path('exams/<int:pk>/delete/',  views.exam_delete, name='exam_delete'),

    # Scores
    path('scores/',                 views.score_list,   name='score_list'),
    path('scores/add/',             views.score_add,    name='score_add'),
    path('scores/<int:pk>/edit/',   views.score_edit,   name='score_edit'),
    path('scores/<int:pk>/delete/', views.score_delete, name='score_delete'),

    # Timetable
    path('timetable/',                  views.timetable_list,   name='timetable_list'),
    path('timetable/add/',              views.timetable_add,    name='timetable_add'),
    path('timetable/<int:pk>/edit/',    views.timetable_edit,   name='timetable_edit'),
    path('timetable/<int:pk>/delete/',  views.timetable_delete, name='timetable_delete'),

    # Notifications
    path('notifications/',                  views.notification_list,   name='notification_list'),
    path('notifications/add/',              views.notification_add,    name='notification_add'),
    path('notifications/<int:pk>/edit/',    views.notification_edit,   name='notification_edit'),
    path('notifications/<int:pk>/delete/',  views.notification_delete, name='notification_delete'),

    # Report Cards
    path('report-cards/',                   views.report_card_list,   name='report_card_list'),
    path('report-cards/add/',               views.report_card_add,    name='report_card_add'),
    path('report-cards/<int:pk>/',          views.report_card_view,   name='report_card_view'),
    path('report-cards/<int:pk>/delete/',   views.report_card_delete, name='report_card_delete'),

    # Events
    path('events/',                 views.event_list,   name='event_list'),
    path('events/add/',             views.event_add,    name='event_add'),
    path('events/<int:pk>/edit/',   views.event_edit,   name='event_edit'),
    path('events/<int:pk>/delete/', views.event_delete, name='event_delete'),

    # Parent portal
    path('parent/attendance/',      views.parent_child_attendance, name='parent_attendance'),
    path('parent/results/',         views.parent_child_results,    name='parent_results'),

    # Student portal
    path('student/attendance/',     views.student_my_attendance,   name='student_attendance'),
    path('student/results/',        views.student_my_results,      name='student_results'),

    # Print Reports
    path('reports/students/',               views.report_students,       name='report_students'),
    path('reports/teachers/',               views.report_teachers,       name='report_teachers'),
    path('reports/attendance/',             views.report_attendance,     name='report_attendance'),
    path('reports/scores/',                 views.report_scores,         name='report_scores'),
    path('reports/student/<int:pk>/',       views.report_student_detail, name='report_student_detail'),
]
