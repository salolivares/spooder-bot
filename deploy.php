<?php
    /**
     * GIT DEPLOYMENT SCRIPT
     *
     * Used for automatically deploying websites via github or bitbucket, more deets here:
     *
     *      https://gist.github.com/1809044
     */

    // The commands
    $commands = array(
        'echo $PWD',
        'whoami',
        'git pull',
        'git status',
        'git submodule sync',
        'git submodule update',
        'git submodule status',
    );

    // Run the commands for output
    $output = '';
    foreach($commands AS $command){
        // Run it
        $tmp = shell_exec($command);
        // Output
        $output .= "<span style=\"color: #6BE234;\">\$</span> <span style=\"color: #729FCF;\">{$command}\n</span>";
        $output .= htmlentities(trim($tmp)) . "\n";
    }

    // Make it pretty for manual user access (and why not?)
?>
<!DOCTYPE HTML>
<html lang="en-US">
<head>
    <meta charset="UTF-8">
    <title>Spooder Bot Deployment Script</title>
</head>
<body style="background-color: #000000; color: #FFFFFF; font-weight: bold; padding: 0 10px;">
<pre>
<?php echo $output; ?>
</pre>
</body>
</html>