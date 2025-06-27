import datetime
from unittest.mock import patch

import testing_data
from geosphere_at_warnings import geosphere


def test_get_relevant_warnings() -> None:
    with patch.object(geosphere, "_fetch_data") as mock_fetch_data:
        mock_fetch_data.return_value = testing_data.get_warnings_for_coords_response_data

        location = geosphere.Location(12.12, 13.13)
        warnings = geosphere.get_relevant_warnings(location)
        mock_fetch_data.assert_called_with(location)

        assert len(warnings.warnings) == 7
        assert warnings.warnings[0].type == geosphere.WarningType.HEAT
        assert warnings.warnings[0].level == geosphere.WarningLevel.ORANGE
        assert warnings.warnings[0].begin == datetime.datetime.fromisoformat("20250626T00:00+02:00")
        assert warnings.warnings[0].end == datetime.datetime.fromisoformat("20250626T23:59+02:00")
        assert warnings.warnings[0].text == "Es ist mit starker Hitzebelastung zu rechnen."
        assert warnings.warnings[0].effects == "* Erhöhte Körpertemperatur\n* Erhöhter Puls\n* Schwäche/Müdigkeit\n* Kopfschmerzen\n* Muskelkrämpfe\n* Trockener Mund und Hals\n* Verwirrtheit, Schwindel, Bewusstseinsstörungen\n* Übelkeit, Erbrechen, Durchfall"
        assert (
            warnings.warnings[0].recommendations
            == "* Meiden Sie direktes Sonnenlicht! Achten Sie darauf, dass Kinder vor der Sonne geschützt sind!\n* Meiden Sie verbaute und versiegelte Plätze wo es keinen Schatten gibt.\n* Gehen Sie nicht in der heißesten Tageszeit nach draußen!\n* Ziehen Sie die Vorhänge zu bzw. schließen Sie die Jalousien. Öffnen Sie die Fenster vorwiegend in der Nacht bzw. in den kühlen Morgenstunden!\n* Vermeiden Sie große Anstrengungen bzw. verschieben Sie körperliche Aktivitäten im Freien auf die frühen Morgenstunden oder den Abend!\n* Tragen Sie luftige, helle Kleidung und eine Kopfbedeckung!\n* Nehmen Sie eine kühle Dusche! Auch kalte Arm- und Fußbäder wirken entlastend.\n* Trinken Sie ausreichend und regelmäßig (mindestens 2 - 3 Liter pro Tag)! Optimal sind Wasser, ungesüßter Tee oder mit Wasser verdünnte Fruchtsäfte.\n* Denken Sie an ältere Mitmenschen und Kinder, dass auch diese regelmäßig trinken. \n* Bevorzugen Sie leichtes Essen!\n* Meiden Sie Alkohol!"
        )


def test_warnings_get_current() -> None:
    now_ = datetime.datetime.now(tz=datetime.UTC)

    warning_current_1 = geosphere.GeosphereWarning(
        type=geosphere.WarningType.HEAT,
        level=geosphere.WarningLevel.YELLOW,
        begin=now_ - datetime.timedelta(hours=1),
        end=now_ + datetime.timedelta(hours=1),
    )

    warning_current_2 = geosphere.GeosphereWarning(
        type=geosphere.WarningType.HEAT,
        level=geosphere.WarningLevel.RED,
        begin=now_ - datetime.timedelta(minutes=1),
        end=now_ + datetime.timedelta(minutes=1),
    )

    warning_future = geosphere.GeosphereWarning(
        type=geosphere.WarningType.HEAT,
        level=geosphere.WarningLevel.ORANGE,
        begin=now_ + datetime.timedelta(hours=1),
        end=now_ + datetime.timedelta(hours=2),
    )

    warning_past = geosphere.GeosphereWarning(
        type=geosphere.WarningType.HEAT,
        level=geosphere.WarningLevel.ORANGE,
        begin=now_ - datetime.timedelta(hours=2),
        end=now_ - datetime.timedelta(hours=1),
    )

    warnings = geosphere.GeosphereWarnings([warning_current_1, warning_current_2, warning_future, warning_past])

    assert warnings.get_relevant(datetime.timedelta(minutes=0)) == [warning_current_1, warning_current_2]


def test_warnings_is_relevant_event_ends_before_now() -> None:
    now_ = datetime.datetime.now(tz=datetime.UTC)

    assert (
        geosphere.GeosphereWarning(
            type=geosphere.WarningType.HEAT,
            level=geosphere.WarningLevel.YELLOW,
            begin=now_ - datetime.timedelta(hours=10),
            end=now_ - datetime.timedelta(hours=5),
        ).is_relevant(advanced_warning_time=datetime.timedelta(hours=1))
        is False
    )


def test_warnings_is_relevant_event_started_before_and_ends_in_advanced_warning_time() -> None:
    now_ = datetime.datetime.now(tz=datetime.UTC)

    assert (
        geosphere.GeosphereWarning(
            type=geosphere.WarningType.HEAT,
            level=geosphere.WarningLevel.YELLOW,
            begin=now_ - datetime.timedelta(hours=5),
            end=now_ + datetime.timedelta(minutes=30),
        ).is_relevant(advanced_warning_time=datetime.timedelta(hours=1))
        is True
    )


def test_warnings_is_relevant_event_started_before_and_ends_after_advanced_warning_time() -> None:
    now_ = datetime.datetime.now(tz=datetime.UTC)
    assert (
        geosphere.GeosphereWarning(
            type=geosphere.WarningType.HEAT,
            level=geosphere.WarningLevel.YELLOW,
            begin=now_ - datetime.timedelta(hours=5),
            end=now_ + datetime.timedelta(hours=10),
        ).is_relevant(advanced_warning_time=datetime.timedelta(hours=1))
        is True
    )


def test_warnings_is_relevant_event_starts_in_advanced_warning_time_and_ends_later() -> None:
    now_ = datetime.datetime.now(tz=datetime.UTC)
    assert (
        geosphere.GeosphereWarning(
            type=geosphere.WarningType.HEAT,
            level=geosphere.WarningLevel.YELLOW,
            begin=now_ + datetime.timedelta(minutes=30),
            end=now_ + datetime.timedelta(hours=10),
        ).is_relevant(advanced_warning_time=datetime.timedelta(hours=1))
        is True
    )


def test_warnings_is_relevant_event_starts_and_ends_in_advanced_warning_time() -> None:
    now_ = datetime.datetime.now(tz=datetime.UTC)
    assert (
        geosphere.GeosphereWarning(
            type=geosphere.WarningType.HEAT,
            level=geosphere.WarningLevel.YELLOW,
            begin=now_ + datetime.timedelta(minutes=30),
            end=now_ + datetime.timedelta(minutes=45),
        ).is_relevant(advanced_warning_time=datetime.timedelta(hours=1))
        is True
    )


def test_warnings_is_relevant_event_starts_after_advanced_warning_time() -> None:
    now_ = datetime.datetime.now(tz=datetime.UTC)
    assert (
        geosphere.GeosphereWarning(
            type=geosphere.WarningType.HEAT,
            level=geosphere.WarningLevel.YELLOW,
            begin=now_ + datetime.timedelta(hours=5),
            end=now_ + datetime.timedelta(hours=10),
        ).is_relevant(advanced_warning_time=datetime.timedelta(hours=1))
        is False
    )
