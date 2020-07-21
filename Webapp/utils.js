module.exports = {

	// Redirect to the given page if authorized
	// If not authorized, redirect to login page
	redirectToPage : function(file,req,res)
	{
		try
		{
			if(req.session.isLoggedIn)
			{
		      res.sendFile(file,{"root":"public"});
		    }
		    else
		    {
		      res.redirect("/")
		    }
		}
		catch(exception)
		{
			res.redirect("/")
		}
	}
}