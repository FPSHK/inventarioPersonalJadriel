import os 

class Config:
    """
    Configuracion general de la aplicacion Flask.
    Puede extenderse a diferentes entornos (Desarrollo, Produccion, etc.) 
    """

    #Clave secreta para proteger sesiones y formularios (CSRF)
    # En producción, se recomienda definir esta variable en el entorno
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave-secreta-flask')

    #URI de conexion a la base de datos 
    #Formato: dialecto+driver://;usuario:contraseña@host/basededatos
    #Ejemplo para MySQl usando PyMySQL (puede adaptarse a PostgreSQL o SQLLite)
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+pymysql://root:@localhost/inventario_personal' #Valor por defecto para entorno local (MAMP/XAMPP)

    )

    #Desactiva el sistema de seguimiento de modificaciones de SQLAlchemy (mejora el rendimiento)
    SQLALCHEMY_TRACK_MODIFICATIONS = False