from app.services.events_service import get_last_event_completed
from app.models import Fight, Event, Fighter, RankingPointsHistoric, Category
from sqlalchemy import func, desc, case, literal_column, Integer
from datetime import datetime


def get_last_event():
    return get_last_event_completed()

def get_last_n_fights(quantity: int = 4):
    return (Fight.query.join(Event, Fight.event_id == Event.id)
                .join(Fighter, Fight.winner_id == Fighter.id or Fight.loser_id == Fighter.id)
                .order_by(Event.id.desc(), Fight.created_at.asc())
                .limit(4)
                .all()
            )

def get_methods_statistics():
    return (Fight.query
                 .join(Event, Fight.event_id == Event.id)
                 .join(Fighter, Fight.winner_id == Fighter.id)
                 .with_entities(Fight.method, func.count(Fight.method).label('count'))
                 .group_by(Fight.method)
                 .all()
            )

def get_pound_4_pound_ranking():
    return (RankingPointsHistoric.query
    .join(Fighter, RankingPointsHistoric.fighter_id == Fighter.id)
    .join(Category, RankingPointsHistoric.category_id == Category.id)
    .filter(Fighter.id == Category.champion_id)
    .with_entities(
        Fighter.name.label('champion_name'),
        Category.description.label('category_name'),
        func.sum(RankingPointsHistoric.points).label('total_points')
    )
    .group_by(Fighter.name, Category.description)
    .order_by(func.sum(RankingPointsHistoric.points).desc())
    .all())


def get_fighter_statistics():
    # Quantidade de Lutas
    most_fights = Fighter.query.with_entities(
        Fighter.id,
        Fighter.name,
        func.count(Fighter.id).label('total_fights')
    ).outerjoin(
        Fight,
        (Fighter.id == Fight.red_corner_id) | (Fighter.id == Fight.blue_corner_id)
    ).group_by(Fighter.id).order_by(desc('total_fights')).first()

    least_fights = Fighter.query.with_entities(
        Fighter.id,
        Fighter.name,
        func.count(Fighter.id).label('total_fights')
    ).outerjoin(
        Fight,
        (Fighter.id == Fight.red_corner_id) | (Fighter.id == Fight.blue_corner_id)
    ).group_by(Fighter.id).order_by('total_fights').first()

    # Vitórias e Derrotas Gerais
    most_victories = Fighter.query.with_entities(
        Fighter.id,
        Fighter.name,
        Fighter.victories
    ).order_by(desc(Fighter.victories)).first()

    most_defeats = Fighter.query.with_entities(
        Fighter.id,
        Fighter.name,
        Fighter.defeats
    ).order_by(desc(Fighter.defeats)).first()

    # Vitórias por Metodo
    most_ko_wins = Fighter.query.with_entities(
        Fighter.id,
        Fighter.name,
        func.count().label('ko_wins')
    ).join(
        Fight,
        ((Fighter.id == Fight.winner_id) & (Fight.method == 'ko'))
    ).group_by(Fighter.id).order_by(desc('ko_wins')).first()

    most_tko_wins = Fighter.query.with_entities(
        Fighter.id,
        Fighter.name,
        func.count().label('tko_wins')
    ).join(
        Fight,
        ((Fighter.id == Fight.winner_id) & (Fight.method == 'tko'))
    ).group_by(Fighter.id).order_by(desc('tko_wins')).first()

    most_submission_wins = Fighter.query.with_entities(
        Fighter.id,
        Fighter.name,
        func.count().label('submission_wins')
    ).join(
        Fight,
        ((Fighter.id == Fight.winner_id) & (Fight.method == 'submission'))
    ).group_by(Fighter.id).order_by(desc('submission_wins')).first()

    most_decision_wins = Fighter.query.with_entities(
        Fighter.id,
        Fighter.name,
        func.count().label('decision_wins')
    ).join(
        Fight,
        ((Fighter.id == Fight.winner_id) &
         (Fight.method.in_(['unanimous_decision', 'majority_decision', 'split_decision'])))
    ).group_by(Fighter.id).order_by(desc('decision_wins')).first()

    # Derrotas por Método
    most_ko_losses = Fighter.query.with_entities(
        Fighter.id,
        Fighter.name,
        func.count().label('ko_losses')
    ).join(
        Fight,
        ((Fighter.id == Fight.loser_id) & (Fight.method == 'KO'))
    ).group_by(Fighter.id).order_by(desc('ko_losses')).first()

    most_tko_losses = Fighter.query.with_entities(
        Fighter.id,
        Fighter.name,
        func.count().label('tko_losses')
    ).join(
        Fight,
        ((Fighter.id == Fight.loser_id) & (Fight.method == 'TKO'))
    ).group_by(Fighter.id).order_by(desc('tko_losses')).first()

    most_submission_losses = Fighter.query.with_entities(
        Fighter.id,
        Fighter.name,
        func.count().label('submission_losses')
    ).join(
        Fight,
        ((Fighter.id == Fight.loser_id) & (Fight.method == 'submission'))
    ).group_by(Fighter.id).order_by(desc('submission_losses')).first()

    most_decision_losses = Fighter.query.with_entities(
        Fighter.id,
        Fighter.name,
        func.count().label('decision_losses')
    ).join(
        Fight,
        ((Fighter.id == Fight.loser_id) &
         (Fight.method.in_(['unanimous_decision', 'majority_decision', 'split_decision'])))
    ).group_by(Fighter.id).order_by(desc('decision_losses')).first()

    # Tempo de Lutas
    shortest_total_fight_time = Fighter.query.with_entities(
        Fighter.id,
        Fighter.name,
        func.sum(
            func.cast(func.strftime('%s', Fight.time), Integer) +
            (Fight.round - 1) * 300
        ).label('total_time')
    ).join(
        Fight,
        (Fighter.id == Fight.red_corner_id) | (Fighter.id == Fight.blue_corner_id)
    ).group_by(Fighter.id).order_by('total_time').first()

    longest_total_fight_time = Fighter.query.with_entities(
        Fighter.id,
        Fighter.name,
        func.sum(
            func.cast(func.strftime('%s', Fight.time), Integer) +
            (Fight.round - 1) * 300
        ).label('total_time')
    ).join(
        Fight,
        (Fighter.id == Fight.red_corner_id) | (Fighter.id == Fight.blue_corner_id)
    ).group_by(Fighter.id).order_by(desc('total_time')).first()

    # Disputas de Título
    most_title_shots = Fighter.query.with_entities(
        Fighter.id,
        Fighter.name,
        func.count().label('title_shots')
    ).join(
        Fight,
        ((Fighter.id == Fight.blue_corner_id)) &
        (Fight.belt_dispute == True)
    ).group_by(Fighter.id).order_by(desc('title_shots')).first()

    most_title_defenses = Fighter.query.with_entities(
        Fighter.id,
        Fighter.name,
        func.count().label('title_defenses')
    ).join(
        Fight,
        (Fighter.id == Fight.winner_id) &
        (Fight.belt_dispute == True)
    ).group_by(Fighter.id).order_by(desc('title_defenses')).first()

    # Finalizações mais Rápidas
    fastest_ko = Fighter.query.with_entities(
        Fighter.id,
        Fighter.name,
        Fight.time,
        Fight.round
    ).join(
        Fight,
        (Fighter.id == Fight.winner_id) & (Fight.method == 'ko')
    ).order_by(
        Fight.round, Fight.time
    ).first()

    fastest_submission = Fighter.query.with_entities(
        Fighter.id,
        Fighter.name,
        Fight.time,
        Fight.round
    ).join(
        Fight,
        (Fighter.id == Fight.winner_id) & (Fight.method == 'submission')
    ).order_by(
        Fight.round, Fight.time
    ).first()

    # Sequências
    def get_streak_subquery(is_current=False, is_victory=True):
        streak_query = Fighter.query.with_entities(
            Fighter.id,
            Fighter.name,
            func.count().label('streak_count')
        ).join(
            Fight,
            (Fighter.id == (Fight.winner_id if is_victory else Fight.loser_id))
        )

        if is_current:
            # Para sequências atuais, precisamos ordenar por data e verificar apenas as lutas mais recentes
            streak_query = streak_query.order_by(Fight.created_at.desc())

        return streak_query.group_by(Fighter.id).order_by(desc('streak_count')).first()

    longest_win_streak = get_streak_subquery(is_current=False, is_victory=True)
    longest_loss_streak = get_streak_subquery(is_current=False, is_victory=False)
    current_win_streak = get_streak_subquery(is_current=True, is_victory=True)
    current_loss_streak = get_streak_subquery(is_current=True, is_victory=False)

    return {
        'most_fights': most_fights,
        'least_fights': least_fights,
        'most_victories': most_victories,
        'most_defeats': most_defeats,
        'most_ko_wins': most_ko_wins,
        'most_tko_wins': most_tko_wins,
        'most_submission_wins': most_submission_wins,
        'most_decision_wins': most_decision_wins,
        'most_ko_losses': most_ko_losses,
        'most_tko_losses': most_tko_losses,
        'most_submission_losses': most_submission_losses,
        'most_decision_losses': most_decision_losses,
        'shortest_total_fight_time': shortest_total_fight_time,
        'longest_total_fight_time': longest_total_fight_time,
        'most_title_shots': most_title_shots,
        'most_title_defenses': most_title_defenses,
        'fastest_ko': fastest_ko,
        'fastest_submission': fastest_submission,
        'longest_win_streak': longest_win_streak,
        'longest_loss_streak': longest_loss_streak,
        'current_win_streak': current_win_streak,
        'current_loss_streak': current_loss_streak
    }
