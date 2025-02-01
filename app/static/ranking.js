document.addEventListener('DOMContentLoaded', function() {
    initializeFightersLinks()
});

function initializeFightersLinks() {
    const fighterLinks = document.querySelectorAll('.fighter-link');

    fighterLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const fighterId = this.getAttribute('data-fighter-id');

            axios.get(`/fighter/${fighterId}/details`)
                .then(response => {
                    const data = response.data;

                    let fights = '';
                    for (const [key, value] of Object.entries(data.fights)) {
                        let color = value.result === 'W' ? 'table-success' : 'table-danger';
                        fights += `
                            <tr class="${color}">
                                <td>${value.result}</td>
                                <td>${value.opponent_name}</td>
                                <td>${value.category_short}</td>
                                <td>${value.event_description.toUpperCase()}</td>
                                <td>${value.method.toUpperCase()}</td>
                                <td>${value.time} / ${value.round}</td>
                            </tr>
                        `
                    }

                    document.getElementById('fighterModalBody').innerHTML = `
                        <div class="fighter-details row">
                            <h4>${data.fighter.name} <small>[${data.fighter.record.cartel} <kbd>${data.fighter.record.only_manager.cartel}</kbd>]</small></h4>
                            <div class="info col-4">
                                <p><span>Age:</span> ${data.fighter.age}</p>
                                <p><span>From:</span> ${data.fighter.from}</p>
                            </div>
                            <div class="col-8">
                                <div class="row text-center">
                                    <div class="col-sm-6">
                                        <div class="result-container win-block">
                                            <div class="text-block px-3 fw-bold">WINS</div>
                                            <div class="px-2 fs-5">${data.fighter.record.only_manager.victories}</div>
                                        </div>
                                    </div>
                                    <div class="col-sm-6">
                                        <div class="result-container lose-block">
                                            <div class="text-block px-3 fw-bold">LOSSES</div>
                                            <div class="px-2 fs-5">${data.fighter.record.only_manager.defeats}</div>
                                        </div>
                                    </div>
                                </div>
                                <div class="row">
                                    <div class="col-sm-6 mt-2 mr-5">          
                                        <div id="win-chart" style="width:260px"></div>
                                    </div>
                                    <div class="col-sm-6 mt-2">                                                
                                        <div id="lose-chart" style="width:260px"></div>
                                    </div>
                                </div>
                            </div>
                            <hr>
                            <h5># Fight History</h5>
                            <div class="row">
                                <div class="container">
                                    <table class="table table-sm">
                                        <thead class="">
                                            <tr>
                                                <th scope="col"></th>
                                                <th scope="col">Opponent</th>
                                                <th scope="col">Category</th>
                                                <th scope="col">Event</th>
                                                <th scope="col">Method</th>
                                                <th scope="col">Time / Round</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            ${fights}
                                        </tbody>
                                    </table>
                                </div>
                            </div>
                        </div>
                    `;

                    const winChartOptions = {
                        chart: {
                          type: 'pie'
                        },
                        series: [data.results.wins.kos, data.results.wins.submissions, data.results.wins.decisions],
                        labels: ['KO / TKO', 'SUBMISSION', 'DECISIONS'],
                        colors: ['#ad2f2f', '#145eac', '#33772e'],
                        legend: {
                            show: false,
                        },
                        tooltip: {
                            enabled: true,
                            hideEmptySeries: false,
                            fillSeriesColor: false,
                            style: {
                              fontSize: '16px',
                              fontFamily: undefined
                            },
                            onDatasetHover: {
                                highlightDataSeries: false,
                            },
                            marker: {
                                show: true,
                            },
                            items: {
                               display: 'flex',
                            },
                            fixed: {
                                enabled: false,
                                position: 'topRight',
                                offsetX: 0,
                                offsetY: 0,
                            }
                        }
                    }

                    const loseChartOptions = {
                        chart: {
                          type: 'pie'
                        },
                        series: [data.results.losses.kos, data.results.losses.submissions, data.results.losses.decisions],
                        labels: ['KO / TKO', 'SUBMISSION', 'DECISIONS'],
                        colors: ['#ad2f2f', '#145eac', '#33772e'],
                        legend: {
                            show: false,
                        },
                        tooltip: {
                            enabled: true,
                            hideEmptySeries: false,
                            fillSeriesColor: false,
                            style: {
                              fontSize: '16px',
                              fontFamily: undefined
                            },
                            onDatasetHover: {
                                highlightDataSeries: false,
                            },
                            marker: {
                                show: true,
                            },
                            items: {
                               display: 'flex',
                            },
                            fixed: {
                                enabled: false,
                                position: 'topRight',
                                offsetX: 0,
                                offsetY: 0,
                            }
                        }
                    }
                      
                    const winChart = new ApexCharts(document.querySelector("#win-chart"), winChartOptions);
                    const loseChart = new ApexCharts(document.querySelector("#lose-chart"), loseChartOptions);
                    
                    winChart.render();
                    loseChart.render();
                })
                .catch(error => {
                    document.getElementById('fighterModalBody').innerHTML = `
                        <div class="alert alert-danger">
                            Erro ao carregar os dados do lutador.
                        </div>
                    `;
                    console.error('Erro:', error);
                });
        });
    });
}
