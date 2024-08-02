import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Table
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy import create_engine
from eralchemy2 import render_er
from datetime import datetime

Base = declarative_base()

# Tabla de asociación para los favoritos
favorito_usuario_personaje = Table('favorito_usuario_personaje', Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuario.id'), primary_key=True),
    Column('personaje_id', Integer, ForeignKey('personaje.id'), primary_key=True)
)

favorito_usuario_planeta = Table('favorito_usuario_planeta', Base.metadata,
    Column('usuario_id', Integer, ForeignKey('usuario.id'), primary_key=True),
    Column('planeta_id', Integer, ForeignKey('planeta.id'), primary_key=True)
)

class Usuario(Base):
    __tablename__ = 'usuario'
    
    id = Column(Integer, primary_key=True)
    email = Column(String(120), unique=True, nullable=False)
    password = Column(String(128), nullable=False)
    nombre = Column(String(50), nullable=False)
    apellido = Column(String(50), nullable=False)
    fecha_suscripcion = Column(String, default=datetime.utcnow().isoformat())
    
    personajes_favoritos = relationship('Personaje', secondary=favorito_usuario_personaje, back_populates='usuarios_favoritos')
    planetas_favoritos = relationship('Planeta', secondary=favorito_usuario_planeta, back_populates='usuarios_favoritos')

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'nombre': self.nombre,
            'apellido': self.apellido,
            'fecha_suscripcion': self.fecha_suscripcion,
            'personajes_favoritos': [p.to_dict() for p in self.personajes_favoritos],
            'planetas_favoritos': [p.to_dict() for p in self.planetas_favoritos]
        }

class Personaje(Base):
    __tablename__ = 'personaje'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    genero = Column(String(50), nullable=True)
    especie = Column(String(50), nullable=True)
    
    usuarios_favoritos = relationship('Usuario', secondary=favorito_usuario_personaje, back_populates='personajes_favoritos')

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'genero': self.genero,
            'especie': self.especie
        }

class Planeta(Base):
    __tablename__ = 'planeta'
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    clima = Column(String(50), nullable=True)
    terreno = Column(String(50), nullable=True)
    
    usuarios_favoritos = relationship('Usuario', secondary=favorito_usuario_planeta, back_populates='planetas_favoritos')

    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'clima': self.clima,
            'terreno': self.terreno
        }

# Define the database URL here
# For example: 'sqlite:///mydatabase.db'
DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///mydatabase.db')
engine = create_engine(DATABASE_URL)

# Create all tables in the database
Base.metadata.create_all(engine)

# Generate the ER diagram
render_er(Base, 'diagram.png')
