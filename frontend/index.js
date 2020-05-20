var ctx = document.getElementById('myChart').getContext('2d');

//

$(".dropdown").change(async (e) => {
    try{
        console.log(e.currentTarget.value)
        ga('send', 'event', 'Select', e.currentTarget.value);
        let data;
        document.getElementById("loading").innerHTML = "loading...";
        await fetch("https://cors-anywhere.herokuapp.com/http://35.193.184.107:5000/get_historical_data?asset_id="+ e.currentTarget.value, {
            headers: {
                // 'Content-Type': 'application/json',
                "Access-Control-Allow-Origin": "*"
            }
        }).then(res => res.json())
        .then(res => data = res.data);
        const time = data ? data.map(item => new Date(item.time_period_start).toDateString()) : [];
        const volume = data ? data.map(item => item.volume_traded) : [];
        document.getElementById("loading").innerHTML = "";
        var myChart = new Chart(ctx, {
            type: 'bar',
            data:  {
                labels: time,
                datasets: [{
                    label: e.currentTarget.value,
                    backgroundColor: '#ff6384',
                    borderColor: '#ff6384',
                    data: volume,
                    fill: false,
                }]
            },
            backgroundColor: 'rgba(1, 0, 1, 0.4)',
            options: {
                scales: {
                    yAxes: [{
                        ticks: {
                            beginAtZero: true
                        }
                    }]
                }
            }
        });
    }catch(err){
        document.getElementById("loading").innerHTML = "error occured";
    }
});


