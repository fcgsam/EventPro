(function($) {
  'use strict';
  $(function() {

    $('#deshbord_date').change(function() {
      // Get the selected date from the input value

      var selectedDate = $(this).val();
      
      // Do something with the selected date, such as displaying it
      console.log('Selected date:', selectedDate.split('-'));
      let currentmount= selectedDate.split('-')[1]
      let currentyr= selectedDate.split('-')[0]

      dashboardData(currentmount,currentyr)
    });
    if($('#deshbord_date').val() == ''){
      console.log("Blank")
      var currentDate = new Date();
      let currentmount= currentDate.getMonth()+1
      let currentyr= currentDate.getFullYear()
      console.log(currentyr)
      dashboardData(currentmount,currentyr)
    }
    function dashboardData(currentmount,currentyr){
    $.ajax({
      url:'/deshboard_data/',
      method:'POST',
      datatype:'json',
      success: function(response) {
        
        var event_data = response.data_chart
        var Title = []
        var event_attendee = []
        var event_budget =[]
        var amount=0
        // var currentDate = new Date();
        // let currentmount= currentDate.getMonth() + 1
        console.log('eventdata',event_data)
        for (let i=0 ; i<event_data.length ;i++){
          
          
          console.log('mounts',event_data[i].date.split('-')[0])
          if (parseInt(event_data[i].date.split('-')[1])==currentmount && event_data[i].date.split('-')[0]==currentyr){
            Title.push(event_data[i].title)
            event_attendee.push(event_data[i].Attendee)
            event_budget.push(event_data[i].Budget)
            amount+=event_data[i].Budget
            console.log("amount data ;",amount)
          }
        }
        event_cart(Title,event_attendee)
        budget_cart(Title,event_budget)
        console.log('amount',amount)
        $('#totalBudgetEvent').text(" $"+amount)
      } ,error: function(xhr, status, error) {
          console.error('Error in deshborad data:', error);
      }

    })
  }
    // console.log(Title)
    function event_cart(Title,event_attendee){
      if (window.marketingOverviewChart) {
        window.marketingOverviewChart.destroy();
    }
      // console.log("num,betr of attend",event_attendee,Math.max(...event_attendee))
      if (event_attendee.length > 0) {
        var maxValue = Math.max.apply(null, event_attendee);
        console.log(maxValue);
      }
      else{
        var maxValue = 0
      }
      if ($("#marketingOverview").length) { 
        const marketingOverviewCanvas = document.getElementById('marketingOverview');
        window.marketingOverviewChart = new Chart(marketingOverviewCanvas, {
          type: 'line',
          data: {
            labels: Title,
            datasets: [{
              label: 'no. of Attendees',
              data: event_attendee,
              borderWidth: 1,
              fill: true, // 3: no fill
              
            }]
          },
  
          options: {
            
            animations: {
              tension: {
                duration: 1000,
                easing: 'linear',
                from: 1,
                to: 0,
                loop: true
              }
            },
            scales: {
              y: {
                grid: {
                  display: false // Remove y-axis grid lines
              },
                ticks: {
                    callback: function(value, index, values) {
                      return value.toLocaleString(undefined, { maximumFractionDigits: 0 }); // Format y-axis number
                    },
                    suggestedMin: 0,
                    maxTicksLimit: maxValue+1
                }
            },
            x:{
              grid: {
                display: false // Remove x-axis grid lines
            },
            },
          
          },
          legend: {
            display: false,
          },

          
          },
          
  
  
        });
      }
    }

    // if ($('#totalVisitors').length) {
    //   var bar = new ProgressBar.Circle(totalVisitors, {
    //     color: '#fff',
    //     // This has to be the same size as the maximum width to
    //     // prevent clipping
    //     strokeWidth: 15,
    //     trailWidth: 15, 
    //     easing: 'easeInOut',
    //     duration: 1400,
    //     text: {
    //       autoStyleContainer: false
    //     },
    //     from: {
    //       color: '#52CDFF',
    //       width: 15
    //     },
    //     to: {
    //       color: '#677ae4',
    //       width: 15
    //     },
    //     // Set default step function for all animate calls
    //     step: function(state, circle) {
    //       circle.path.setAttribute('stroke', state.color);
    //       circle.path.setAttribute('stroke-width', state.width);
  
    //       var value = Math.round(circle.value() * 100);
    //       if (value === 0) {
    //         circle.setText('');
    //       } else {
    //         circle.setText(value);
    //       }
  
    //     }
    //   });
  
    //   bar.text.style.fontSize = '0rem';
    //   bar.animate(.64); // Number from 0.0 to 1.0
    // }

    // if ($('#visitperday').length) {
    //   var bar = new ProgressBar.Circle(visitperday, {
    //     color: '#fff',
    //     // This has to be the same size as the maximum width to
    //     // prevent clipping
    //     strokeWidth: 15,
    //     trailWidth: 15,
    //     easing: 'easeInOut',
    //     duration: 1400,
    //     text: {
    //       autoStyleContainer: false
    //     },
    //     from: {
    //       color: '#34B1AA',
    //       width: 15
    //     },
    //     to: {
    //       color: '#677ae4',
    //       width: 15
    //     },
    //     // Set default step function for all animate calls
    //     step: function(state, circle) {
    //       circle.path.setAttribute('stroke', state.color);
    //       circle.path.setAttribute('stroke-width', state.width);
  
    //       var value = Math.round(circle.value() * 100);
    //       if (value === 0) {
    //         circle.setText('');
    //       } else {
    //         circle.setText(value);
    //       }
  
    //     }
    //   });
  
    //   bar.text.style.fontSize = '0rem';
    //   bar.animate(.34); // Number from 0.0 to 1.0
    // }

    function budget_cart(Title,event_budget){
      if ($("#doughnutChart").length) { 
        const doughnutChartCanvas = document.getElementById('doughnutChart');
        if (window.marketingOverviewChartDo) {
          window.marketingOverviewChartDo.destroy();
      }


      window.marketingOverviewChartDo = new Chart(doughnutChartCanvas, {
          type: 'doughnut',
          data: {
            labels: Title,
            datasets: [{
              data: event_budget,
              // backgroundColor: [
              //   "#1F3BB3",
              //   "#FDD0C7",
              //   "#52CDFF",
              //   "#81DADA"
              // ],
              // borderColor: [
              //   "#1F3BB3",
              //   "#FDD0C7",
              //   "#52CDFF",
              //   "#81DADA"
              // ],
            }]
          },
          options: {
            cutout: 90,
            animationEasing: "easeOutBounce",
            animateRotate: true,
            animateScale: false,
            responsive: true,
            maintainAspectRatio: true,
            showScale: true,
            legend: false,
            plugins: {
              legend: {
                  display: false,
              }
            }
          },
  
        });
      }
    }
    

    // if ($("#leaveReport").length) { 
    //   const leaveReportCanvas = document.getElementById('leaveReport');
    //   new Chart(leaveReportCanvas, {
    //     type: 'bar',
    //     data: {
    //       labels: ["Jan","Feb", "Mar", "Apr", "May"],
    //       datasets: [{
    //           label: 'Last week',
    //           data: [18, 25, 39, 11, 24],
    //           backgroundColor: "#52CDFF",
    //           borderColor: [
    //               '#52CDFF',
    //           ],
    //           borderWidth: 0,
    //           fill: true, // 3: no fill
    //           barPercentage: 0.5,
    //       }]
    //     },
    //     options: {
    //       responsive: true,
    //       maintainAspectRatio: false,
    //       elements: {
    //         line: {
    //             tension: 0.4,
    //         }
    //     },
    //       scales: {
    //         yAxes: {
    //           display: true,
    //           grid: {
    //             display: false,
    //             drawBorder: false,
    //             color:"rgba(255,255,255,.05)",
    //             zeroLineColor: "rgba(255,255,255,.05)",
    //           },
    //           ticks: {
    //             beginAtZero: true,
    //             autoSkip: true,
    //             maxTicksLimit: 5,
    //             fontSize: 10,
    //             color:"#6B778C",
    //             font: {
    //               size: 10,
    //             }
    //           }
    //         },
    //         xAxes: {
    //           display: true,
    //           grid: {
    //             display: false,
    //           },
    //           ticks: {
    //             beginAtZero: false,
    //             autoSkip: true,
    //             maxTicksLimit: 7,
    //             fontSize: 10,
    //             color:"#6B778C",
    //             font: {
    //               size: 10,
    //             }
    //           }
    //         }
    //       },
    //       plugins: {
    //         legend: {
    //             display: false,
    //         }
    //       }
    //     }
    //   });
    // }

    
  });
  // iconify.load('icons.svg').then(function() {
  //   iconify(document.querySelector('.my-cool.icon'));
  // });
  
  
  // $("#datepicker").datepicker({
  //   changeMonth: false,
  //   changeYear: true,
  //   showButtonPanel: true,
  //   dateFormat: 'yy',
  //   onClose: function(dateText, inst) { 
  //     var year = $("#ui-datepicker-div .ui-datepicker-year :selected").val();
  //     $(this).datepicker('setDate', new Date(year, 1));
  //   }
  // });

})(jQuery);

