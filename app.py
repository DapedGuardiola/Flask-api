from flask import Flask
from config import Config
from dotenv import load_dotenv
import pandas as pd
import redis
import mysql.connector
import os
from app.routes.saw_routes import saw_bp
from app.routes.edas_routes import edas_bp
from app.routes.cbf_routes import cbf_bp
from app.routes.compute_routes import compute_bp
from extension import r
import json

app = Flask(__name__)
app.register_blueprint(saw_bp)
app.register_blueprint(edas_bp)
app.register_blueprint(cbf_bp)
app.register_blueprint(compute_bp)


def warm_up_global_cache():
    try:
        if r.exists('movie_discover_data'):
            return True
        conn = mysql.connector.connect(
            host = os.getenv('DB_HOST','localhost'),
            port = int(os.getenv('DB_PORT',3306)),
            database = os.getenv('DB_DATABASE','mysql'),
            user = os.getenv('DB_USERNAME','root'),
            password = os.getenv('DB_password',None),
        )
        query = """
        SELECT 
            m.tmdb_movie_id, 
            v.vector, 
            n.n_popularity, 
            n.n_rating 
        FROM movies m 
        JOIN movie_genre_vector v ON v.tmdb_movie_id = m.tmdb_movie_id 
        JOIN normalized_movie n ON n.tmdb_movie_id = m.tmdb_movie_id 
        """
        df = pd.read_sql(query,conn)
        conn.close()
        if df.empty:
            print("❌ db dengan vector dan normalized data kosong") 
            return False
        df['vector'] = df['vector'].apply(json.loads)
        df_json = df.to_json(orient='split')
        r.set('movie_discover_data',df_json)
        return True
    except Exception as e:
        print(f"❌ Gagal memuat data & konfigurasi: {str(e)}")
        return False
    
with app.app_context():
    warm_up_global_cache()

@app.route('/ping', methods=['GET'])
def ping():
    return {'status': 'ok', 'message': 'Flask is running'}

if __name__ == '__main__':
    app.run(debug=Config.Debug,
            port=Config.PORT)