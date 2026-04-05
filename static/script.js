//定义在index.html中引用的脚本文件
function askQuestion() {
    const question = document.getElementById("questionInput").value;
    const status=document.getElementById("status");
    const answerDiv = document.getElementById("answerOutput");

    status.innerText = "thinking...";
    answerDiv.innerText =""; 

    fetch("/api/ask", {
        method:"POST",
        headers: {
            "Content-Type": "application/json"
        },
        //这句跟在mainBody.py里的一句对应
        //question = request.json.get('question')
        body: JSON.stringify({ question: question })
    })
    .then (response => {
            if(!response.ok) {
                throw new Error("Network response was not ok");
            }
            //返回json格式的回答
            return response.json();
    }
        //拿到真正数据后显示
     ).then (data => {
            //清空状态
            status.innerText = "";
            //显示答案
            answerDiv.innerText = data.answer;
            return data;
    }

        //捕捉错误
    ).catch (error => {
            //如果有error，让函数status显示error，并在控制台打印错误
            status.innerText = "Error: ";
            console.error(error);
        });

}

function clearQuestion() {
    document.getElementById("questionInput").value = "";
}
