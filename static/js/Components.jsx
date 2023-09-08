function App(){
    return(
        <nav className = "nav">
            <a href="/user_profile/<int:user_id>" className ="user-profile">User Profile</a> 
            <ul>
                <li><a href="/get_meals">Get Some Ideas</a></li>
                <li><a href="/create_a_meal">Add Your Own Dish</a></li>
                <li><a href="/">Log Out To Start Cooking</a></li>
            </ul>
        </nav>
    )
}

ReactDOM.render(<App />, document.getElementById('navroot'));