from datetime import datetime
from typing import List, Optional
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Integer, Float, Text, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(80), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    first_name: Mapped[Optional[str]] = mapped_column(String(80))
    last_name: Mapped[Optional[str]] = mapped_column(String(80))
    is_active: Mapped[bool] = mapped_column(Boolean(), nullable=False, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    favorite_characters: Mapped[List["FavoriteCharacter"]] = relationship(back_populates="user")
    favorite_planets: Mapped[List["FavoritePlanet"]] = relationship(back_populates="user")

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            # do not serialize the password, its a security breach
        }


class Planet(db.Model):
    __tablename__ = "planet"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    climate: Mapped[Optional[str]] = mapped_column(String(120))
    terrain: Mapped[Optional[str]] = mapped_column(String(120))
    population: Mapped[Optional[int]] = mapped_column(Integer)
    diameter: Mapped[Optional[int]] = mapped_column(Integer)
    gravity: Mapped[Optional[str]] = mapped_column(String(50))
    rotation_period: Mapped[Optional[int]] = mapped_column(Integer)
    orbital_period: Mapped[Optional[int]] = mapped_column(Integer)
    description: Mapped[Optional[str]] = mapped_column(Text)
    image_url: Mapped[Optional[str]] = mapped_column(String(255))

    residents: Mapped[List["Character"]] = relationship(back_populates="homeworld")
    favorited_by: Mapped[List["FavoritePlanet"]] = relationship(back_populates="planet")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "climate": self.climate,
            "terrain": self.terrain,
            "population": self.population,
            "diameter": self.diameter,
            "gravity": self.gravity,
            "rotation_period": self.rotation_period,
            "orbital_period": self.orbital_period,
            "description": self.description,
            "image_url": self.image_url,
        }


class Character(db.Model):
    __tablename__ = "character"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    gender: Mapped[Optional[str]] = mapped_column(String(30))
    birth_year: Mapped[Optional[str]] = mapped_column(String(30))
    height: Mapped[Optional[int]] = mapped_column(Integer)
    mass: Mapped[Optional[float]] = mapped_column(Float)
    hair_color: Mapped[Optional[str]] = mapped_column(String(50))
    eye_color: Mapped[Optional[str]] = mapped_column(String(50))
    skin_color: Mapped[Optional[str]] = mapped_column(String(50))
    description: Mapped[Optional[str]] = mapped_column(Text)
    image_url: Mapped[Optional[str]] = mapped_column(String(255))
    homeworld_id: Mapped[Optional[int]] = mapped_column(ForeignKey("planet.id"))

    homeworld: Mapped[Optional["Planet"]] = relationship(back_populates="residents")
    favorited_by: Mapped[List["FavoriteCharacter"]] = relationship(back_populates="character")

    def serialize(self):
        return {
            "id": self.id,
            "name": self.name,
            "gender": self.gender,
            "birth_year": self.birth_year,
            "height": self.height,
            "mass": self.mass,
            "hair_color": self.hair_color,
            "eye_color": self.eye_color,
            "skin_color": self.skin_color,
            "description": self.description,
            "image_url": self.image_url,
            "homeworld_id": self.homeworld_id,
        }


class FavoriteCharacter(db.Model):
    __tablename__ = "favorite_character"
    __table_args__ = (UniqueConstraint("user_id", "character_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    character_id: Mapped[int] = mapped_column(ForeignKey("character.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="favorite_characters")
    character: Mapped["Character"] = relationship(back_populates="favorited_by")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "character_id": self.character_id,
        }


class FavoritePlanet(db.Model):
    __tablename__ = "favorite_planet"
    __table_args__ = (UniqueConstraint("user_id", "planet_id"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    planet_id: Mapped[int] = mapped_column(ForeignKey("planet.id"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    user: Mapped["User"] = relationship(back_populates="favorite_planets")
    planet: Mapped["Planet"] = relationship(back_populates="favorited_by")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "planet_id": self.planet_id,
        }
