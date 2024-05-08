from website import create_app

def enumerate_filter(iterable):
    return enumerate(iterable)

if __name__ == '__main__':
    app = create_app()
    # Register the custom filter
    app.jinja_env.filters['enumerate'] = enumerate_filter
    
    app.run(debug=True)
