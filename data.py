from datetime import datetime
import sqlite3

class WorkoutData:
    def __init__(self, db_file="workouts.db"):
        self.conn = sqlite3.connect(db_file)
        self.cursor = self.conn.cursor()
        self._create_tables()

    def _create_log_tables(self):
        # Table for routines: day, movement, sets, reps
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS logs (
                day TEXT,
                movement TEXT,
                sets INTEGER,
                reps INTEGER,
                PRIMARY KEY(day, movement)
            )
        """)
        self.conn.commit()

    def _create_tables(self):
        # Table for routines: day, movement, sets, reps
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS routines (
                day TEXT,
                movement TEXT,
                sets INTEGER,
                reps INTEGER,
                PRIMARY KEY(day, movement)
            )
        """)
        self.conn.commit()

    def save_routine(self, day_name, movements_dict):
        """Save a routine to the database, replacing existing ones. Blank movements are removed."""
        # Delete movements that aren't in the new dict
        if movements_dict:
            placeholders = ",".join("?" for _ in movements_dict)
            self.cursor.execute(
                f"DELETE FROM routines WHERE day = ? AND movement NOT IN ({placeholders})",
                (day_name, *movements_dict.keys())
            )
        else:
            # If the new routine is empty, remove all entries for that day
            self.cursor.execute("DELETE FROM routines WHERE day = ?", (day_name,))

        # Insert or update movements from the new routine
        for movement, (sets, reps) in movements_dict.items():
            self.cursor.execute("""
                INSERT INTO routines (day, movement, sets, reps)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(day, movement) DO UPDATE SET
                    sets=excluded.sets,
                    reps=excluded.reps
            """, (day_name, movement, sets, reps))

        self.conn.commit()

    def movements(self):
        return ["Pushups", "Pike Pushups", "Weighted Pushups", "Dips",
                "Squats", "Pull ups", "Dead Hangs", "Tricep Dips",
                "Slow Negatives", "Australian Rows", "Plank", "Dip Holds",
                "Knee Raises",
                ]

    def load_routine(self, day_name):
        """Return a dict {movement: (sets, reps)} for the given day."""
        self.cursor.execute("SELECT movement, sets, reps FROM routines WHERE day = ?", (day_name,))
        rows = self.cursor.fetchall()
        return {movement: (sets, reps) for movement, sets, reps in rows}

    def close(self):
        self.conn.close()
