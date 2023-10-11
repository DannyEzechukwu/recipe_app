// Nav Bar

function NavComponent(){
    const [userId, seUserId] = React.useState(0);
    const [userName, setUserName] = React.useState("");

    React.useEffect(() => {
        fetch("/get_user_id/json")
          .then((response) => response.json())
          .then((data) => {
            seUserId(data.user_id)
            setUserName(data.user_name)
        });
      }, [userId, userName]);

      const user_profile_url = `/user_profile/${userId}`;
      

    return(
        <nav className = "nav">
            <a href={user_profile_url} className ="user-profile-option">{userName}'s Profile</a> 
            <ul className="other-options">
                <li><a href="/get_meals" id="get_meals">Get Meal Ideas</a></li>
                <li><a href="/create_a_meal" id="create_a_meal">Add Your Own Dish</a></li>
                <li><a href="/" id="log_out">Log Out And Start Cooking</a></li>
            </ul>
        </nav>
    )
}

ReactDOM.render(<NavComponent />, document.getElementById('navroot'));

