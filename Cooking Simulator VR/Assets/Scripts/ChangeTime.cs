using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI; // Required when Using UI elements.
using TMPro;

public class ChangeTime : MonoBehaviour
{
    public Slider mainSlider;
    public TextMeshProUGUI sliderText;

    // Start is called before the first frame update
    void Start()
    {
        mainSlider.onValueChanged.AddListener (delegate {ValueChangeCheck ();});
    }

    public void ValueChangeCheck()
	{
        sliderText.text = "Selected Time: " + mainSlider.value.ToString("0") + " min";
    }
}
