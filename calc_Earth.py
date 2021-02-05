import spiceypy
import datetime
import math

spiceypy.furnsh('_kernels/lsk/naif0012.tls')
spiceypy.furnsh('_kernels/spk/de432s.bsp')

DATE_TODAY = datetime.datetime.today()

DATE_TODAY = DATE_TODAY.strftime('%Y-%m-%dT00:00:00')

ET_TODAY_MIDNIGHT = spiceypy.utc2et(DATE_TODAY)

print(ET_TODAY_MIDNIGHT)

EARTH_STATE_WRT_SUN, EARTH_SUN_LT = spiceypy.spkgeo(targ=399, et= ET_TODAY_MIDNIGHT,
                                                    ref= 'ECLIPJ2000', obs=10)

print(EARTH_STATE_WRT_SUN, EARTH_SUN_LT)
EARTH_SUN_DISTANCE = math.sqrt(EARTH_STATE_WRT_SUN[0]**2.0 
                             + EARTH_STATE_WRT_SUN[1]**2.0 
                             + EARTH_STATE_WRT_SUN[2]**2.0)

EARTH_SUN_DISTANCE_AU = spiceypy.convrt(EARTH_SUN_DISTANCE, 'km', 'AU')

print('Current distance between the Earth and the Sun in AU:', 
      EARTH_SUN_DISTANCE_AU)

EARTH_ORB_SPEED_WRT_SUN = math.sqrt(EARTH_STATE_WRT_SUN[3]**2.0 
                                  + EARTH_STATE_WRT_SUN[4]**2.0 
                                  + EARTH_STATE_WRT_SUN[5]**2.0)

# It's around 30 km/s
print('Current orbital speed of the Earth around the Sun in km/s:', 
      EARTH_ORB_SPEED_WRT_SUN)

spiceypy.furnsh('_kernels/pck/gm_de431.tpc')
_, GM_SUN = spiceypy.bodvcd(bodyid=10, item='GM', maxn=1)

# Now compute the orbital speed
V_ORB_FUNC = lambda gm, r: math.sqrt(gm/r)

EARTH_ORB_SPEED_WRT_SUN_THEORY = V_ORB_FUNC(GM_SUN[0], EARTH_SUN_DISTANCE)

# Print the result
print('Theoretical orbital speed of the Earth around the Sun in km/s:', 
      EARTH_ORB_SPEED_WRT_SUN_THEORY)