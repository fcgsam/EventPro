$(document).ready(function() {

    $('table.display').DataTable(
      {
      language: { search: '<i class="icon-search"></i>', searchPlaceholder: "Search..." },    
    }
    );
   

    $(".dropdown-menu a").click(function(){
        var selectedText = $(this).text();
        $(".dropdown-toggle").text(selectedText);
      });

        function getTomorrowDate() {
            const tomorrow = new Date();
            tomorrow.setDate(tomorrow.getDate() + 1);
    
            const year = tomorrow.getFullYear();
            const month = (tomorrow.getMonth() + 1).toString().padStart(2, '0');
            const day = tomorrow.getDate().toString().padStart(2, '0');
    
            return `${year}-${month}-${day}`;
        }
    
        $('#example_id').attr('min', getTomorrowDate());
        $('#edit_date').attr('min', getTomorrowDate());
    
        $(document).on('click', '#EventTable tbody tr', function() {
            var cells = $(this).find('td');
            // var currentDate = new Date()

//             const options = { month: 'long', day: 'numeric', year: 'numeric' };

// // Format the date using toLocaleDateString() with the specified options
//             const editdate = date.toLocaleDateString('en-US', options);

//             console.log(editdate,cells.eq(3).text());
            var dateObject = new Date(cells.eq(3).text());
          //   if (dateObject < currentDate) {

          //     console.log('yess the date',dateObject,currentDate)
          //     if(!$('save_edit').length){$('#save_edit').remove()}
              

          // }
          // else{
          //   let button = $("<Button>").attr("type", "submit").attr('id','save_edit').attr("class","btn btn-primary").text("Save");
          //   if($('#save_edit').length === 0){$('#Edit_model_event').append(button)}
            
          // }
            var day = dateObject.getDate().toString().padStart(2, '0');
            var month = (dateObject.getMonth() + 1).toString().padStart(2, '0');
            var year = dateObject.getFullYear();
            var formattedDate = year + '-' + month + '-' + day;
    
            var timeString = cells.eq(4).text();
            var timeComponents = timeString.match(/(\d+):(\d+)\s?([aApP]\.?[mM]\.?)/);
    
            if (!timeComponents) {
                return null;
            }
    
            var hours = parseInt(timeComponents[1], 10);
            var minutes = parseInt(timeComponents[2], 10);
            var period = timeComponents[3].toLowerCase();
    
            if (period === 'p' && hours < 12) {
                hours += 12;
            } else if (period === 'a' && hours === 12) {
                hours = 0;
            }
            
            var managedBy = cells.eq(7).text();
            var pic = cells.eq(7).data("pic");
            console.log("Pic:", pic);
            const img = $('<img>', {
                    src: pic, 
                    alt: 'profile Img',
                    class: 'rounded-circle me-1',
                    width: 24, 
                    height: 24
            });

            $('#imgspan_editEvent').empty();
            $('#imgspan_editEvent').append(img,managedBy);
            var formattedTime = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:00`;
            // console.log("data for maneger : ",val(cells.eq(7).text()))
            $('#floatingInputTitle').val(cells.eq(0).text());
            $('#Description_id').val(cells.eq(1).text());
            $('#floatingTextareavenue').val(cells.eq(2).text());
            $('#edit_date').val(formattedDate);
            $('#edit_time').val(formattedTime);
            if (cells.eq(6).text() == 'Completed'){
              console.log("if part disabled")
              var newInput = $("<input>").attr("type", "hidden").attr("name", "edit_budget").attr('id','new_edit_budget');
              $('#Edit_model_event').append(newInput)
              newInput.val($(this).data("budget"))
              $('#floatingInputBudget').attr('name',"edit_budget1")
              $('#floatingInputBudget').prop('disabled', true);

              $('#floatingInputBudget').val($(this).data("budget"));
            }else{
              console.log("else part disabled")
              $('#floatingInputBudget').prop('disabled', false);
              if (!$('#new_edit_budget').length) {
              $('#new_edit_budget').remove()
              }
              $('#floatingInputBudget').attr('name',"edit_budget")
              $('#floatingInputBudget').val($(this).data("budget"));
            }
            
            $('#Status_edit').val(cells.eq(6).text());
            $('#edit_assgin_to_email').val($(this).data("email"));
            $('#edit_event_name_id').val($(this).data("name"));
            console.log("manegd : : : :",$(this).data("budget"))
            $('#floatingInputAttendee').val(cells.eq(8).text());
            var clickedRowId = $(this).data("id");
            console.log(clickedRowId);
            var clickedRowtitle = $(this).data("title");
            $('#edit_id_input').val(clickedRowId);
            $('.spain_class').text(clickedRowtitle);
            $('#popup_delete').val(clickedRowId);

        });
        $(document).on('click', '#TaskTable tbody tr', function() {
            var cells = $(this).find('td');
    
            var clickedRowId = $(this).data("id");
            var status = $(this).data("status");
            var clickedRowtitle = $(this).data("title");
            var clickedRowemail = $(this).data("email");
            let budget = $(this).data("budget");
            $('.new_task_title').text(clickedRowtitle);
            $('#new_task_id').val(clickedRowId);
            $('#event_status').val(status)
            $('#new_task_email').val(clickedRowemail);
            $('#event_budget').val(budget);
            console.log(" task status :: ",status)
            if (status == 'Completed'){
                $('#completedInput').prop('checked', true);
              
            }else{
                $('#completedInput').prop('checked', false)
            }
            $.ajax({
                url: '/task_table/',
                method: 'POST',
                data:{
                  event_id: clickedRowId,
              },
                dataType: 'json',
                success: function(response) {
                  let task = response.task
                  let total_sum = response.total_sum
                  let today_date = response.TodayDate
                  console.log(total_sum)
                  // if(total_sum<1){
                    $('#totla_amount').text(total_sum)

                  if(budget<total_sum){
                    if (!$('#ammount_mssg').length) {
                    $('#statusAndamount').append('<p class="card col" style="background-color: red; padding-top: 6px;" id="ammount_mssg">You exceeded the allocated amount!</p>');
                    }
                  }else{
                    $('#ammount_mssg').remove();
                  }
                  $('#NewTak tbody').empty();
                  $('#taskTable tbody').empty();
                  for (var i = 0; i < task.length; i++) {
                    
                      if(clickedRowId == task[i].Event_id ){    
                        console.log(clickedRowId,today_date)
                        
                        var newRow = $('<tr id="budg-'+task[i].id+'" data-id="'+task[i].id+'" data-title="'+task[i].title+'" data-budget="'+task[i].Budget+'"">');
                        newRow.append($('<td>').text(task[i].title));
                        newRow.append($('<td>').text(task[i].Budget));
                        if (!today_date.includes(clickedRowId)) {
                          newRow.append($('<td>').html('<button type="button" class="btn btn-primary" id="Edit_model_popup_try"><i class="mdi mdi-pencil menu-icon icon-xl"></i></button><button type="button" class="btn btn-danger" id="Delete_model_popup_try"><i class="mdi mdi-delete-outline icon-xl"></i></button>'));
                          // Remove #create_task if it exists
                          if (!$('#completedInput').length && !$('#create_task').length){
                          var submit_button = $('<input>').attr('type','checkbox').attr('class','form-check-input').attr('id','completedInput').attr('role','switch');
                          $('#statusAndamount').append(submit_button);
                          var budget_button = $('<button>').attr('type','button').attr('class','btn btn-primary col-sm-2').attr('onclick','addtask()').attr('id','create_task').text('Create');
                          // Append budget_button
                          $('#task_budget_btn').append(budget_button);
                          }
                      } else if(today_date.includes(clickedRowId)) {
                          
                        if ($('#create_task').length) {
                          $('#create_task').remove();
                        }
                        if ($('#completedInput').length) {
                            $('#completedInput').remove();
                        }
                      }
                        $('#NewTak tbody').append(newRow);
                    } 
                    
                        // console.log('bububububuAdmin =',task[i].Budget)
                        // var newRow = $('<tr id="budg-'+task[i].id+'" data-id="'+task[i].id+'" data-title="'+task[i].title+'" data-budget="'+task[i].Budget+'"">');
                        // newRow.append($('<td>').text(task[i].title));
                        // newRow.append($('<td>').text(task[i].Budget));
                        // newRow.append($('<td>').html('<button type="button" class="btn btn-primary" id="Edit_model_popup_try"><i class="mdi mdi-pencil menu-icon icon-xl"></i></button><button type="button" class="btn btn-danger" id="Delete_model_popup_try"><i class="mdi mdi-delete-outline icon-xl"></i></button>'));
                        // $('#NewTakAdmin tbody').append(newRow);
               
                  }
                  if ($.fn.DataTable.isDataTable('#NewTak')) {
                    $('#taskTable').DataTable().draw();
                    
                  } else {
                    $('#NewTak').DataTable({
                      language: { search: '<i class="icon-search"></i>', searchPlaceholder: "Search..." },
                    });
                  }
                },
                error: function() {
                  console.error('Error fetching data from /task_table/');
                }
              });
            // $.ajax({
            //     url: '/total_amount/',
            //     method: 'POST',
            //     data: {
            //         event_id: clickedRowId,
            //         // status:'Completed',
            //     },
            //     dataType: 'json',
            //     success: function(response) {
            //         console.log("Total Amount for this : ",response.total_sum)
            //         },
            //     error: function(xhr, status, error) {
            //             console.error('Error updating total:', error);
            //     }
            // });

        });
        $(document).on('click', '#NewTak tbody tr', function() {
          // $('.task_spain_class').text()
          console.log($(this).data("title"))
          $('#delete_span_id').text($(this).data("title"))
          $('.delete_task_id').val($(this).data("id"))
          $('.amount_id').val($(this).data("budget"))
          console.log('budgdgdgdg = =',$(this).data("title"))
          let cells = $(this).find('td');
          $('#Edit_task_title').val(cells.eq(0).text());
          $('#edit_task_budget').val(cells.eq(1).text());
          cells.eq(0).text($('#Edit_task_title').val())
          cells.eq(1).text($('#edit_task_budget').val())
        })
        $(document).on('click', '#Edit_model_popup_try', function() {
          // Open the edit_model modal when the edit button is clicked
          $('#edit_model').modal('show');
        });
        $(document).on('click', '#Delete_model_popup_try', function() {
          // Open the edit_model modal when the edit button is clicked
          
          $('#delete_model').modal('show');
          
        });

        $('#completedInput').change(function() {
          if ($(this).is(':checked')) {
            
            $.ajax({
              url: '/update_status/',
              method: 'POST',
              
              data: {
                  event_id: $('#new_task_id').val(),
                  status:'Completed',
              },
              dataType: 'json',
              success: function(response) {
                  console.log($('#completedInput'))
                  },
              error: function(xhr, status, error) {
                      console.error('Error updating task:', error);
                }
                });
                }else{
                  console.log('Else not checked')
                  $.ajax({
                    url: '/update_status/',
                    method: 'POST',
                    
                    data: {
                        event_id: $('#new_task_id').val(),
                        status:'Ongoing',
                    },
                    dataType: 'json',
                    success: function(response) {
                        console.log($('#completedInput'))
                        // if (response.status === 'success') {
                        //     // Optionally, perform actions after successful update
                        //   $('#completedInput').prop('checked', true);
                        // } else {
                        //     console.error('Error updating task:', response.message);
                        // }
                        },
                    error: function(xhr, status, error) {
                            console.error('Error updating task:', error);
                      }
                      });
                }
              })     
              
});