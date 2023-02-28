using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI; // Required when Using UI elements.
using TMPro;

public class GameOver : MonoBehaviour
{
    public TextMeshProUGUI gameOverText;

    // Start is called before the first frame update
    void Start()
    {
       gameOverText.text = ""; 
    }
}
