from app.services.storyboard import generate_storyboard

def test_two_panel_script():
    sb = generate_storyboard("A cat steals fish from a market stall.", 2)
    assert len(sb.panels) == 2
    assert sb.panels[0].scene
    assert sb.panels[0].dialogue
