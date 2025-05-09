from app import app, db
from models import User, Movie, Showtime, Seat, Reservation, Payment, Admin, AdminReference
from datetime import datetime, timedelta
import random

def seed_data():
    # Ensure database tables are created
    with app.app_context():
        db.create_all()

        # Seed an admin user
        if not User.query.filter_by(username="Admin Thomus").first():
            admin = User(
                username="Admin Thomus",
                email="adminthomas827@gmail.com",  # Admin email
                role="admin"
            )
            admin.set_password("Thomas9699.")
            db.session.add(admin)

        # Seed regular users
        user1 = User.query.filter_by(username="Davincii 254").first()
        if not user1:
            user1 = User(
                username="Davincii 254",
                email="davincii25411@gmail.com"  # User1 email
            )
            user1.set_password("Davincii254.")
            db.session.add(user1)

        user2 = User.query.filter_by(username="Bin Amin").first()
        if not user2:
            user2 = User(
                username="Bin Amin",
                email="binamin12@gmail.com"  # User2 email
            )
            user2.set_password("Binamin12.")
            db.session.add(user2)

        db.session.flush()  # To update the session with the new users

        # Genres for movies
        genres = ["Action", "Comedy", "Drama", "Horror", "Sci-Fi"]

        # Seed movies (2 per genre, 10 total)
        for genre in genres:
            for i in range(1, 3):  # Only 2 movies per genre now
                movie_title = f"{genre} Movie {i}"
                movie_description = f"A thrilling {genre.lower()} movie with gripping moments."
                movie = Movie.query.filter_by(title=movie_title).first()
                if not movie:
                    movie = Movie(
                        title=movie_title,
                        description=movie_description,
                        genre=genre,
                        poster_url="https://via.placeholder.com/150",  # Placeholder image URL
                        release_date=datetime.now().date() - timedelta(days=random.randint(1, 365))  # Random past date
                    )
                    db.session.add(movie)
                    db.session.flush()  # Save the movie to get its ID

                    # Seed showtimes for each movie (3 showtimes per movie)
                    for j in range(3):  # Reduced to 3 showtimes per movie
                        start_time = datetime.now() + timedelta(days=j, hours=random.randint(1, 3))
                        showtime = Showtime(
                            movie_id=movie.id,
                            start_time=start_time,
                            duration=random.randint(90, 180)  # Random duration between 90 and 180 minutes
                        )
                        db.session.add(showtime)
                        db.session.flush()  # Save the showtime to get its ID

                        # Seed 20 seats per showtime
                        for seat_num in range(1, 21):  # 20 seats per showtime
                            row = "ABCDE"[seat_num // 5]  # Rows A-E
                            column = seat_num % 5 or 5  # Columns 1-5
                            seat = Seat(
                                seat_number=f"{row}{column}",
                                row=row,
                                column=column,
                                showtime_id=showtime.id,
                                is_reserved=False
                            )
                            db.session.add(seat)

        db.session.flush()

        # Seed reservations for user1 on some showtimes and seats
        showtimes = Showtime.query.limit(5).all()
        for showtime in showtimes:
            reservation = Reservation(user_id=user1.id, showtime_id=showtime.id)
            db.session.add(reservation)
            db.session.flush()  # Save the reservation to get its ID

            # Reserve first 3 seats for this reservation
            seats = Seat.query.filter_by(showtime_id=showtime.id).limit(3).all()
            for seat in seats:
                seat.is_reserved = True
                reservation.seats.append(seat)

            # Optionally seed a payment for the reservation
            payment = Payment(
                user_id=user1.id,
                reservation_id=reservation.id,
                amount=random.uniform(10.0, 50.0),  # Random amount between 10 and 50
                payment_method="M-Pesa",  # For example, or choose from other methods
                status="completed"
            )
            db.session.add(payment)

        # Commit all changes
        db.session.commit()
        print("Database seeded with movies, showtimes, seats, reservations, and payments.")

if __name__ == '__main__':
    seed_data()
    print("Database seeding completed!")