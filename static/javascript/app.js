// let commentButon = document.querySelectorAll(".comment-button");
let newCommentArea = document.querySelectorAll(".comment-section");
let threadContainer = document.querySelectorAll(".thread-container");

// step 1 identificate all the places where the listener should be added

function createCommentDiv(json_response){
    //Creates a comment based on detail.html
    
    return `<!-- start of comment header section   -->
                <div class="card-body  py-0 ">
                <div class="row comment-header">
                    <div class="col-10">
                        <a class="text-decoration-none text-reset text-xxs" href="/users/${ json_response.data.user_id }"> 
                        <small class="text-subtle"><b>${json_response.data.user_username}</b> commented:</small>
                        </a>
                    </div>
                    <div class="col-2 text-right ">
                        <small class="muted text-subtle text-xxs"> <i> now </i></small>
                    </div>
                    
                </div> 
                <!-- start of comment content section -->
                <div class="row ">
                <div class="col-12 comment-body">
                    <p class="text-left">${json_response.data.content}</p>
                    </div>  
                </div>
            </div>`;
}




async function sendCommentToServer(userID, threadID, comment){
    
    let response = await axios.post(`http://127.0.0.1:5000/comments/`, 
                                    {user_id:userID, thread_id:threadID, comment:comment},
                                    {headers: {'Content-Type': 'application/json'}});  
    
    return createCommentDiv(response);
};


threadContainer.forEach(function(button){

    button.addEventListener('click', async function(e){
        
        if (e.target.classList.contains("comment-button")){
            
            cardBody = e.target.parentElement.parentElement;
            inputDiv = e.target.parentElement;
            
            inputDiv.innerHTML =`<div class="input-group input-group-sm mb-3">
                                    <input type="text" class="form-control bg-dark comment-input" placeholder="Write your comment here" aria-label="Recipient's username" aria-describedby="button-addon2">
                                    <div class="input-group-append">
                                        <button class="btn btn-outline-secondary comment-send-button" type="button" id="button-addon2">Comment</button>
                                    </div>
                                </div>`;
            cardBody.append(inputDiv);
        }
    
        else if (e.target.classList.contains("comment-send-button")){
            
            // this is to get the content of the input
            let parentDiv = e.target.parentElement.parentElement;
            let input = parentDiv.querySelector(".comment-input");
            
            if (input.value){
                
                let greatGrandParentDiv = parentDiv.parentElement;
                let userID =  greatGrandParentDiv.getAttribute("user_id");
                let threadID = greatGrandParentDiv.getAttribute("thread_id");
                let serverResponse = await sendCommentToServer(userID, threadID, input.value);
                let thisThreadContainer = greatGrandParentDiv.closest('.thread-container');
                
                let commentSection = thisThreadContainer.querySelector('.comment-container');

                let newDiv = document.createElement("div");
                newDiv.className = "card text-white";
                newDiv.innerHTML = serverResponse;
                commentSection.append(newDiv);
                
                input.value = '';
            }
        }
    
    });       
});

// I will repeat the function in order to also incorporate the "return" in the input field
// I could have done it in a more synthetical way, but I don't have time