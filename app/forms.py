from flask_wtf import FlaskForm
from wtforms import (StringField, IntegerField, DecimalField,
                     SelectField, DateField, PasswordField, SubmitField)
from wtforms.validators import DataRequired, Optional, NumberRange, Email, Length


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Usuario', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Contraseña', validators=[DataRequired(), Length(min=6)])
    role = SelectField('Rol', choices=[
        ('Admin', 'Admin'),
        ('Usuario', 'Usuario'),
        ('Owner', 'Owner')
    ])
    submit = SubmitField('Registrarse')


class ItemForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired()])
    categoria = SelectField('Categoría', choices=[
        ('Electrónica', 'Electrónica'),
        ('Ropa', 'Ropa'),
        ('Hogar', 'Hogar'),
        ('Deportes', 'Deportes'),
        ('Libros', 'Libros'),
        ('Otro', 'Otro')
    ], validators=[DataRequired()])
    cantidad = IntegerField('Cantidad', validators=[DataRequired(), NumberRange(min=1)])
    precio_estimado = DecimalField('Precio Estimado ($)', validators=[Optional()], places=2)
    ubicacion = StringField('Ubicación', validators=[Optional()])
    fecha_adquisicion = DateField('Fecha de Adquisición', validators=[Optional()])
    submit = SubmitField('Guardar')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Contraseña Actual', validators=[DataRequired()])
    new_password = PasswordField('Nueva Contraseña', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Cambiar Contraseña')
