using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;
using TMPro;

public class FoodChecker : MonoBehaviour
{
    public List<GameObject> foodObjects;
    public TextMeshProUGUI gameOverText;
    private PiledChecker piledCheckerScript;
    public DisplayTimer gameTimer;
    public GameObject menu;

    // Start is called before the first frame update
    void Start()
    {
        piledCheckerScript = GetComponent<PiledChecker>();
    }

    // Update is called once per frame
    void Update()
    {
        if (isPileCorrect()) {
            menu.SetActive(true);
            gameOverText.text = "Hamburger Done!";
            DisplayTimer gT = gameTimer.GetComponent<DisplayTimer>();
            gT.StopTimer();
        }
    }

    bool isPileCorrect() {
        List<GameObject> objectsPiledOnTop = new List<GameObject>();
        objectsPiledOnTop = piledCheckerScript.GetObjectsPiledOnTop();

        if (objectsPiledOnTop.Count != foodObjects.Count) return false;

        for (var i = 0; i < objectsPiledOnTop.Count; i++) {
            string foodName1 = objectsPiledOnTop[i].GetComponent<FoodDescription>().GetFoodName();
            string foodName2 = foodObjects[i].GetComponent<FoodDescription>().GetFoodName();

            if (foodName1 != foodName2) return false;
        }

        return true;
    }
}
