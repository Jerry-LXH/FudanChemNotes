import sqlite3
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d

class FilterDatabaseSQLite:
    """An object that connects/creates a SQLITE database and offers methods to manipulate the tables stored there."""
    def __init__(self, db_file="filters.db"):
        self.conn = sqlite3.connect(db_file)
        self.conn.execute("PRAGMA foreign_keys = ON;") 
        self._create_tables()

    def _create_tables(self):
        """2 tables for filter and spectra seperately, connected by foreign key. (totally 4+2 input for a filter)"""
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS filters (
                id INTEGER PRIMARY KEY,
                name TEXT UNIQUE,
                type TEXT,
                manufacturer TEXT,
                notes TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS spectra (
                id INTEGER PRIMARY KEY,
                filter_id INTEGER,
                wavelength REAL,
                transmission REAL,
                FOREIGN KEY(filter_id) REFERENCES filters(id) ON DELETE CASCADE
            )
        ''')
        self.conn.commit()

    def add_filter(self, name, wavelengths, transmissions, ftype="Unknown", manufacturer="", notes="", overwrite=False):
        """name, ftype, manufacturer and notes should be string; wavelength and transmissions should be lists of numbers of same length"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM filters WHERE name=?", (name,))
        row = cursor.fetchone()
        if row:
            filter_id = row[0]
            if overwrite:
                cursor.execute("DELETE FROM spectra WHERE filter_id=?", (filter_id,))
                cursor.execute('''
                    UPDATE filters SET type=?, manufacturer=?, notes=? WHERE id=?
                ''', (ftype, manufacturer, notes, filter_id))
                print(f"!! Filter '{name}' already exists, overwriting data.")
            else:
                print(f"!! Filter '{name}' already exists, no data updated.")
                return
        else:
            cursor.execute('''
                INSERT OR IGNORE INTO filters (name, type, manufacturer, notes)
                VALUES (?, ?, ?, ?)
            ''', (name, ftype, manufacturer, notes))
            self.conn.commit()

            cursor.execute("SELECT id FROM filters WHERE name=?", (name,))
            filter_id = cursor.fetchone()[0]
            print(f"New filter '{name}' is added.")

        cursor.executemany('''
            INSERT INTO spectra (filter_id, wavelength, transmission)
            VALUES (?, ?, ?)
        ''', [(filter_id, float(wl), float(tr)) for wl, tr in zip(wavelengths, transmissions)])
        self.conn.commit()

    def search(self, keyword):
        """search with name/type/manufacturer/notes"""
        cursor = self.conn.cursor()
        cursor.execute('''
            SELECT * FROM filters WHERE name LIKE ? OR type LIKE ? OR manufacturer LIKE ? OR notes LIKE ?
        ''', (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
        return cursor.fetchall()

    def get_filter_spectrum(self, name):
        """get a spectrum of filter with its name"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id FROM filters WHERE name=?", (name,))
        result = cursor.fetchone()
        if not result:
            return None, None
        filter_id = result[0]

        cursor.execute("SELECT wavelength, transmission FROM spectra WHERE filter_id=? ORDER BY wavelength", (filter_id,))
        data = cursor.fetchall()
        if not data:
            return None, None

        wavelengths, transmissions = zip(*data)
        return np.array(wavelengths), np.array(transmissions)
    
    def delete_filter(self, name):
        """delete by name"""
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM filters WHERE name=?", (name,))
        self.conn.commit()
        print(f"滤镜 {name} 已删除")

    def list_all_filters(self, order_by="manufacturer"):
        """list all filters by manufacturer and type"""
        cursor = self.conn.cursor()
        if order_by not in ("manufacturer", "type", "name", "id"):
            order_by = "manufacturer"
        query = f"SELECT id, name, type, manufacturer, notes FROM filters ORDER BY {order_by} COLLATE NOCASE"
        cursor.execute(query)
        results = cursor.fetchall()
        if not results:
            print("There is no records in database.")
            return []
        print(f"Ordered by: {order_by} :")
        for fid, name, ftype, manufacturer, notes in results:
            print(f"ID={fid}, 名称={name}, 类型={ftype}, 厂商={manufacturer}, 备注={notes}")
        return results