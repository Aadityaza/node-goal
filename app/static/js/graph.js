document.getElementById('node-form').addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form from submitting the traditional way

    let formData = {
        'content': document.getElementById('content').value,
        'tag': document.getElementById('tag').value
    };

    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(formData)
    })
    .then(response => response.json())
    .then(data => {
        // Update graph here
        updateGraph();
    })
    .catch(error => console.error('Error:', error));
});

function updateGraph() {
    fetch('/graph_data')
        .then(response => response.json())
        .then(data => {
            // Use the data to update the graph in the 'graph-container'
            document.getElementById('graph-container').innerHTML = /* logic to create graph from data */;
        })
        .catch(error => console.error('Error:', error));
}

// Optionally, set an interval to refresh the graph periodically
setInterval(updateGraph, 5000); // Update every 5 seconds
