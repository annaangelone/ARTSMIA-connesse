from database.DB_connect import DBConnect
from model.artObject import ArtObject
from model.connessioni import Connessione

class DAO():

    @staticmethod
    def getAllObjects():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "SELECT * FROM objects"
        cursor.execute(query, )

        for row in cursor:
            result.append(ArtObject(**row))
            # equivale a creare il costruttore lungo con tutte le righe con i rispettivi attributi

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getAllConnessioni(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("""SELECT eo1.object_id as o1, eo2.object_id as o2, count(*) as peso
                    FROM exhibition_objects eo1, exhibition_objects eo2
                    WHERE eo1.exhibition_id = eo2.exhibition_id and eo1.object_id < eo2.object_id
                    GROUP BY eo1.object_id, eo2.object_id
                    ORDER BY peso DESC""")
        cursor.execute(query, )

        for row in cursor:
            result.append(Connessione(idMap[row["o1"]], idMap[row["o2"]], row["peso"]))
            # equivale a creare il costruttore lungo con tutte le righe con i rispettivi attributi

        cursor.close()
        conn.close()
        return result


    @staticmethod
    def getPeso(v1: ArtObject, v2: ArtObject):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = ("""SELECT count(*) 
                    FROM exhibition_objects eo1, exhibition_objects eo2
                    WHERE eo1.exhibition_id = eo2.exhibition_id and eo1.object_id < eo2.object_id
                    AND eo1.object_id = %s AND eo2.object_id = %s""")

        cursor.execute(query, (v1.object_id, v2.object_id,))

        for row in cursor:
            result.append(row)
            # equivale a creare il costruttore lungo con tutte le righe con i rispettivi attributi

        cursor.close()
        conn.close()
        return result
