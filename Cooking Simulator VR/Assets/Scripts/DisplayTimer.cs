using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class DisplayTimer : MonoBehaviour {

    public TMP_Text textTimer;
    public TextMeshProUGUI gameOverText;
    public GameObject menu;

    public float timer = 0.0f;
    public bool isRunning = false;
    public float starterTimer = 10.0f * 60;

    void Start() {
        timer = starterTimer;
    }

    // Update is called once per frame
    void Update() {
        if (isRunning) {
            timer -= Time.deltaTime;

            if (timer <= 0) {
              StopTimer();
              ResetTimer();
              TimerFinished();
            }

            DisplayTime();
        }
    }

    void DisplayTime() {
        int minutes = Mathf.FloorToInt(timer / 60.0f);
        int seconds = Mathf.FloorToInt(timer - minutes * 60);
        textTimer.text = string.Format("{0:00}:{1:00}", minutes, seconds);
    }

    public void SetTimer(float new_timer) {
        timer = new_timer * 60;
        starterTimer = new_timer * 60; 
    }

    public void StartTimer() {
        isRunning = true;
    }

    public void StopTimer() {
        isRunning = false;
    }

    public void ResetTimer() {
        timer = starterTimer;
    }

    public void TimerFinished() {
        gameOverText.text = "Game Over";
        menu.SetActive(true);
    }
}
