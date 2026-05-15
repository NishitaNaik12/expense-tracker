from app import create_app, db

app = create_app()

# This ensures tables are created in production on Render/Supabase
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
