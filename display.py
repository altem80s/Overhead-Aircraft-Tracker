"""Pygame display for an HDMI-connected screen."""
import pygame

class AircraftDisplay:
    def __init__(self, width=800, height=480, fullscreen=True):
        pygame.init()
        flags = pygame.FULLSCREEN if fullscreen else 0
        self.screen = pygame.display.set_mode((width, height), flags)
        pygame.display.set_caption("Overhead Aircraft Tracker")
        self.width, self.height = width, height
        self.clock = pygame.time.Clock()
        scale = min(width/800, height/480)
        self.title = pygame.font.Font(None, max(28, int(40*scale)))
        self.large = pygame.font.Font(None, max(28, int(38*scale)))
        self.medium = pygame.font.Font(None, max(21, int(26*scale)))
        self.small = pygame.font.Font(None, max(17, int(19*scale)))
        self.bg, self.panel = (9,17,29), (17,31,48)
        self.accent, self.white = (67,210,170), (238,244,250)
        self.muted, self.warning = (143,163,183), (255,190,90)

    def text(self, value, font, color, x, y, max_width=None):
        original = str(value)
        value = original
        if max_width:
            while value and font.size(value)[0] > max_width:
                value = value[:-1]
            if value != original and len(value) > 3:
                value = value[:-3] + "..."
        self.screen.blit(font.render(value, True, color), (x,y))

    def draw(self, data, countdown=30):
        self.screen.fill(self.bg)
        margin = max(18, int(self.width*.035))
        width = self.width - 2*margin
        self.text("OVERHEAD AIRCRAFT TRACKER", self.title, self.white, margin, 18)
        status_color = self.accent if data["status"] == "AIRCRAFT OVERHEAD" else self.warning
        self.text(data["status"], self.small, status_color, margin, 65)
        top, height = 100, self.height-178
        pygame.draw.rect(self.screen, self.panel, (margin,top,width,height), border_radius=14)
        self.text(data["callsign"], self.large, self.accent, margin+20, top+18, width-40)
        self.text(data["aircraft_type"], self.medium, self.white, margin+20, top+65, width-40)
        self.text("REGISTRATION  "+data["registration"], self.small,
                  self.muted, margin+20, top+105)
        gap, cell_w = 14, (width-68)//3
        metrics = [("ALTITUDE",data["altitude"]),("GROUND SPEED",data["speed"]),
                   ("HEADING",data["heading"]),("DISTANCE",data["distance"]),
                   ("UPDATED",data["updated"]),("NEXT REFRESH",f"{countdown}s")]
        for i,(label,value) in enumerate(metrics):
            row,col = divmod(i,3)
            x,y = margin+20+col*(cell_w+gap), top+155+row*72
            self.text(label,self.small,self.muted,x,y)
            self.text(value,self.medium,self.white,x,y+25,cell_w)
        self.text("LIVE ADS-B DATA  |  NOT FOR NAVIGATION",self.small,
                  self.muted,margin,self.height-55)
        pygame.display.flip()

    def tick(self):
        self.clock.tick(10)

    def close(self):
        pygame.quit()
