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
import traceback
print("🚀 main.py loaded")
app = Flask(__name__)
app.register_blueprint(saw_bp)
app.register_blueprint(edas_bp)
app.register_blueprint(cbf_bp)
app.register_blueprint(compute_bp)


print("🚀 before warm up")
def warm_up_global_cache():
    try:
        if r.exists('movie_normalized_data'):
            return True
        conn = mysql.connector.connect(
            host = os.getenv('DB_HOST','localhost'),
            port = int(os.getenv('DB_PORT',3306)),
            database = os.getenv('DB_DATABASE','mysql'),
            user = os.getenv('DB_USERNAME','root'),
            password = os.getenv('DB_PASSWORD',None),
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
        r.set('movie_normalized_data',df_json)
        
        from app.service.similar_movie_service import get_all_similar_movies
        all_similar = get_all_similar_movies()
        if all_similar:
            print("data cache berhasil disimpan")
        
        return True
    except Exception as e:
        print(f"❌ Gagal memuat data & konfigurasi: {str(e)}")
        traceback.print_exc()  # ← tambah ini, tampilkan detail error
        return False

print("🚀 after warm up")
    
    
with app.app_context():
    warm_up_global_cache()

@app.route('/ping', methods=['GET'])
def ping():
    return {'status': 'ok', 'message': 'Flask is running'}

if __name__ == '__main__':
    app.run(debug=Config.Debug,
            port=Config.PORT)