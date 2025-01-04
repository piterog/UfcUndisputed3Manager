from app.controllers import home_controller, fights_controller, fighters_controller, events_controller

def register_routes(app):
    app.add_url_rule('/home', 'home', home_controller.index, methods=['GET'])
    app.add_url_rule('/fighters', 'fighters', fighters_controller.index, methods=['GET'])
    app.add_url_rule('/events', 'events', events_controller.index, methods=['GET'])
    app.add_url_rule('/event', 'event', events_controller.create_event, methods=['GET', 'POST'])
    app.add_url_rule('/event/<int:event_id>', 'event_build', events_controller.event_build)
    app.add_url_rule('/event/<int:event_id>/awards', 'event_awards', events_controller.event_awards, methods=['GET'])
    app.add_url_rule('/event/<int:event_id>/awards', 'event_awards_save', events_controller.event_awards_save, methods=['POST'])
    app.add_url_rule('/event/<int:event_id>', 'event_schedule', events_controller.event_schedule, methods=['POST'])
    app.add_url_rule('/event/<int:event_id>/fights', 'event_fights', events_controller.event_fights)
    app.add_url_rule('/event/<int:event_id>/fight/<int:fight_id>', 'fight_save_results', fights_controller.fight_save_results, methods=['POST'])
    app.add_url_rule('/fighters/<int:category_id>/category', 'fighters_by_categorys', fighters_controller.fighters_by_category, methods=['GET'])
    app.add_url_rule('/teste', 'teste', fights_controller.teste, methods=['GET'])