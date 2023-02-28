using System.Collections;
using System.Collections.Generic;
using UnityEngine;

public class PiledChecker : MonoBehaviour {

    public GameObject belowOf;

    public bool drawRay = false;

    private Vector3 center;

    // Start is called before the first frame update
    void Start() {
        center = GetComponent<Collider>().bounds.center;
    }

    // Update is called once per frame
    void FixedUpdate() {
        center = GetComponent<Collider>().bounds.center;

        RaycastHit hit;

        if (drawRay)
          Debug.DrawRay(center, Vector3.up, Color.green);

        if(Physics.Raycast(center, Vector3.up, out hit,  0.1f)) {
            //Debug.Log(gameObject.name + " is below of " + hit.transform.gameObject);

            belowOf = hit.transform.gameObject;
        } else {
            belowOf = null;
        }
    }

    public GameObject GetObjectOnTop() {
        return belowOf;
    }

    public List<GameObject> GetObjectsPiledOnTop() {
        List<GameObject> objectsPiledOnTop = new List<GameObject>();
        GameObject obj = belowOf;

        while (true) {
            if (obj == null) break;

            PiledChecker piledCheckerScript = obj.GetComponent<PiledChecker>();
            if (piledCheckerScript == null) break;

            if (objectsPiledOnTop.Contains(obj)) break;

            objectsPiledOnTop.Add(obj);

            obj = piledCheckerScript.GetObjectOnTop();
        }

        return objectsPiledOnTop;
    }
}
