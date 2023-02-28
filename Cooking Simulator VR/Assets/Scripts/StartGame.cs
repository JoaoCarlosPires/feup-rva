using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class StartGame : MonoBehaviour
{
    public Button startGameButton;
    public DisplayTimer gameTimer;
    public Slider sliderTime;
    public GameObject menu;
    public TextMeshProUGUI gameOverText;
    public ResetPosition breadDown;
    public ResetPosition breadUp;
    public ResetPosition lettuce;
    public ResetPosition tomato;
    public ResetPosition cheese;
    public ResetPosition meat;

    // Start is called before the first frame update
    void Start()
    {
        Button btn = startGameButton.GetComponent<Button>();
		btn.onClick.AddListener(TaskOnClick);
    }

    void TaskOnClick(){
        DisplayTimer gT = gameTimer.GetComponent<DisplayTimer>();
        gT.SetTimer(sliderTime.value);
        gT.StartTimer();

        menu.SetActive(false);
        gameOverText.text = "";

        breadDown.ResetOriginalPosition();
        breadUp.ResetOriginalPosition();
        lettuce.ResetOriginalPosition();
        tomato.ResetOriginalPosition();
        cheese.ResetOriginalPosition();
        meat.ResetOriginalPosition();
    }
}
