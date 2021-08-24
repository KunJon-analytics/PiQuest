from user.models import User
from classroom.models import (ClassAnswer, Course, MyFile, Lesson, ClassQuestion, ClassQuiz, Student,
                              StudentAnswer, Subject, Teacher)
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from django.forms.utils import ValidationError
from django.forms.widgets import TextInput


class AdminAddForm(UserCreationForm):
    email = forms.EmailField()
    last_name = forms.CharField(max_length=80)
    first_name = forms.CharField(max_length=80)

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'last_name', 'first_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_staff = True
        if commit:
            user.save()
        return user


class BaseAnswerInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_answer = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_answer = True
                    break
        if not has_one_correct_answer:
            raise ValidationError(
                'Mark at least one answer as correct.', code='no_correct_answer')


class CourseAddForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    code = forms.CharField(max_length=20, label='Course Code')
    description = forms.CharField(
        widget=forms.Textarea(), max_length=1000, label='Short Description')
    image = forms.ImageField(
        help_text='Recommended image resolution: 740px x 480px. This field is required.')

    class Meta:
        model = Course
        fields = ('title', 'code', 'description', 'subject', 'image')

    def __init__(self, *args, **kwargs):
        super(CourseAddForm, self).__init__(*args, **kwargs)
        # Gets all the subjects and order it by name
        self.fields['subject'].queryset = self.fields['subject'].queryset \
            .all().order_by('name')


class FileAddForm(forms.ModelForm):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}),
                           help_text='Allowed file formats: .pdf, .doc, .docx, .ppt, and .pptx.')

    class Meta:
        model = MyFile
        fields = ('file', 'course')

    def __init__(self, current_user, *args, **kwargs):
        super(FileAddForm, self).__init__(*args, **kwargs)
        # Gets all the courses and order it by name
        self.fields['course'].queryset = self.fields['course'].queryset \
            .filter(owner=current_user) \
            .exclude(status__iexact='deleted') \
            .order_by('title')


class LessonAddForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    number = forms.IntegerField(max_value=20, label='Lesson No.',
                                help_text='This helps the ordering of your lessons in the display.')
    description = forms.CharField(
        widget=forms.Textarea(), label='Short Description', max_length=1000)
    content = forms.Textarea()

    class Meta:
        model = Lesson
        fields = ('title', 'number', 'description', 'content', 'course')

    def __init__(self, current_user, *args, **kwargs):
        super(LessonAddForm, self).__init__(*args, **kwargs)
        # Gets only the courses that the logged in teacher owns and order it by title
        self.fields['course'].queryset = self.fields['course'].queryset \
            .filter(owner=current_user.id) \
            .exclude(status__iexact='deleted') \
            .order_by('title')


class LessonEditForm(forms.ModelForm):
    title = forms.CharField(max_length=100)
    number = forms.IntegerField(max_value=20, label='Lesson No.',
                                help_text='This helps the ordering of your lessons in the display.')
    description = forms.CharField(
        widget=forms.Textarea(), max_length=500, label='Short Description')
    content = forms.Textarea()

    class Meta:
        model = Lesson
        fields = ('title', 'number', 'description', 'content')


class QuizAddForm(forms.ModelForm):
    title = forms.CharField(widget=forms.TextInput(
        attrs={'autocomplete': 'off'}))

    class Meta:
        model = ClassQuiz
        fields = ('title', 'course', 'lesson')

    def __init__(self, current_user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Gets only the courses that the logged in teacher owns and exclude the deleted:
        self.fields['course'].queryset = self.fields['course'] \
            .queryset.filter(owner=current_user.id) \
            .exclude(status__iexact='deleted') \
            .order_by('title')
        # The lesson field is dependent on course field
        self.fields['lesson'].queryset = Lesson.objects.none()

        if 'course' in self.data:
            try:
                course_id = int(self.data.get('course'))
                self.fields['lesson'].queryset = Lesson.objects.filter(
                    course_id=course_id).order_by('title')
            except (ValueError, TypeError):
                pass  # invalid input from the client; ignore and fallback to empty Lesson queryset
        elif self.instance.pk:
            self.fields['lesson'].queryset = self.instance.course.lesson_set.order_by(
                'title')


class QuizEditForm(forms.ModelForm):
    title = forms.CharField(max_length=255,
                            widget=forms.TextInput(attrs={'autocomplete': 'off'}))

    class Meta:
        model = ClassQuiz
        fields = ('title', )


class QuestionForm(forms.ModelForm):
    text = forms.CharField(widget=forms.TextInput(
        attrs={'autocomplete': 'off'}))

    class Meta:
        model = ClassQuestion
        fields = ('text', )


class SearchCourses(forms.ModelForm):
    search = forms.CharField(widget=forms.TextInput(
        attrs={'placeholder': 'Enter your keywords here...'}), label='')

    class Meta:
        model = Course
        fields = ('search', )


class SubjectUpdateForm(forms.ModelForm):
    name = forms.CharField(max_length=30, label='Subject')

    class Meta:
        model = Subject
        fields = ('name', 'color')
        widgets = {
            'color': TextInput(attrs={'type': 'color'}),
        }


class StudentInterestsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('interests', )
        widgets = {
            'interests': forms.CheckboxSelectMultiple
        }


class StudentProfileForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['image']


class TakeQuizForm(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=ClassAnswer.objects.none(),
        widget=forms.RadioSelect(),
        required=True,
        empty_label=None)

    class Meta:
        model = StudentAnswer
        fields = ('answer', )

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('id')


class TeacherProfileForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ('image', )
