from discord.ext import commands

authorized_users = [
    "140350353521639424",  # Sal
    "140208896726925312"   # Elijah
]

def checkIfOwner(message):
    """A helper function used by isOwner()."""
    return message.author.id in authorized_users


def isOwner():
    """Checks if the author of the message is the owner of the server.
    Essentially checks if author is a superadmin or spooderBot developer."""
    return commands.check(lambda ctx: checkIfOwner(ctx.message))
