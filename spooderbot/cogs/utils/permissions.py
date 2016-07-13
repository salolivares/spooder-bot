from discord.ext import commands

authorizedUsers = [
    "140350353521639424",  # Sal
    "140208896726925312"   # Elijah
]

def checkIfOwner(message):
    """A helper function used by isOwner()."""
    return message.author.id in authorizedUsers


def isOwner():
    """Checks if the author of the message is the owner of the server.
    Essentially checks if author is a superadmin."""
    return commands.check(lambda ctx: checkIfOwner(ctx.message))
