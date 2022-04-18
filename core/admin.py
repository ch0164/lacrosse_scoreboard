from django.contrib import admin

import core.models as core
import user_registration.models as registration

admin.site.register(core.Roster)
admin.site.register(core.Coach)
admin.site.register(core.Scorekeeper)
admin.site.register(core.Player)
admin.site.register(core.PlayerStatistics)

admin.site.register(core.Scorebook)
admin.site.register(core.Score)
admin.site.register(core.RunningScore)
admin.site.register(core.Timeout)
admin.site.register(core.TimeoutSet)
admin.site.register(core.Penalty)
admin.site.register(core.PenaltySet)

admin.site.register(registration.CustomUser)

