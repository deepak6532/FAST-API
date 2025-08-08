from fastapi import FastAPI
from pydantic import BaseModel



app = FastAPI()


class Todo_Type(BaseModel):
    id:int
    name: str
    age: int
    email:str
    password:str


@app.get("/")
def  read_first():
    return {"message":"Hello fastapi"}


@app.get("/setname/{name}")
def set_name(name: str):
    return {"message":f"Hello {name}"}


@app.post("/sendname")
def send_name(name: str,age :int,email:str,password:str):  # send data using params
       
    
    print(f"Name: {name}, Age: {age}, Email: {email}, Password: {password}")
    return {"message":f"Name: {name}, Age: {age}, Email: {email}, Password: {password}"}
    
 
 
 
 
 
#  Curd Operation  for Todo 

   
todos = []


@app.post("/addtodo")
def add_todo(todo:Todo_Type):
    
    todos.append(todo)
    
    return {"message":"Todo added successfully", "todo": todo}



@app.get("/gettodo")
def get_todo():
    return {"todos":todos}


@app.put("/updatetodo/{id}")
def update_todo(id:int,update_data_item:Todo_Type):
    for i,todo in enumerate(todos):
          if todo.id == id:
                todos[i] = update_data_item
                return {"message":"Todo updated successfully", "todo": update_data_item}
    return {"message":"Todo not found"}
    


@app.delete("/deletetodo/{id}")
def delete_todo(id:int):
    for i,todo in enumerate(todos):
        if todo.id == id:
            del todos[i]
            return {"message":"Todo delted succeessfully"}
        
    return {"message":"Todo not found"}



# delete all the data with the same id 

@app.delete("/deletetodo/{id}")
def delete_todo(id: int):
    global todos
    original_len = len(todos)
    todos = [todo for todo in todos if todo.id != id]

    if len(todos) < original_len:
        return {"message": f"Todos with id {id} deleted successfully."}
    else:
        return {"message": "Todo not found."}
    
    
    
