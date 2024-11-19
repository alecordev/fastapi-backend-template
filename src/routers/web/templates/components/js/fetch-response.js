function fetchResponse(URLEndpoint, ...elementIds) {
    const requestData = {};

    elementIds.forEach(id => {
        const element = document.getElementById(id);
        if (element) {
            requestData[id] = element.value;
        }
    });

    console.log("Sending payload: \n" + JSON.stringify(requestData));

    fetch(URLEndpoint, {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "x-api-key": "dummy"
        },
        body: JSON.stringify(requestData)
    })
        .then(response => response.json())
        .then(data => {
            processResponse(data);
        })
        .catch(error => {
            console.error("Error: ", error);
        })
        .finally(() => {
            console.log("Request complete.");
        })
};
