#from . import stage
import stage

class Phenology(object):
    def __init__(self, timestep):
        self.timestep = timestep
        self.setup()

    def setup(self):
        # mean growing season temperature since germination, SK 1-19-12
        self.gst_tracker = gstt = stage.GstTracker(self)
        self.gdd_tracker = gddt = stage.GddTracker(self)
        self.gti_tracker = gtit = stage.GtiTracker(self)

        self.germination = g = stage.Germination(self)
        self.emergence = e = stage.Emergence(self)
        self.leaf_initiation = li = stage.LeafInitiation(self)
        self.leaf_appearance = la = stage.LeafAppearance(self)
        self.tassel_initiation = ti = stage.TasselInitiation(self)
        self.silking = s = stage.Silking(self)
        self.grain_filling_initiation = gfi = stage.GrainFillingInitiation(self)
        self.mature = m = stage.Mature(self)
        #self.maturity = m = Maturity(self)

        self.phyllochrons_from_ti = pti = stage.PhyllochronsFromTI(self)

        self.stages = [
            gstt, gddt, gtit,
            g, e, li, la, ti, s, gfi, m,
            pti,
        ]

    def __getitem__(self, index):
        return self.stages[index]

    def _queue(self):
        return [s for s in self.stages if s.ready() and not s.over()]

    def update(self, T):
        queue = self._queue()

        [s.update(T) for s in queue]
        [s.post_update() for s in queue]

        #FIXME remove finish() for simplicity
        [s.finish() for s in queue if s.over()]

    ############
    # Accessor #
    ############

    @property
    def leaves_total(self):
        return self.leaf_initiation.leaves

    @property
    def leaves_generic(self):
        #TODO from TInitInfo
        return 15

    @property
    def leaves_initiated(self):
        return self.leaf_initiation.leaves

    @property
    def leaves_appeared(self):
        return self.leaf_appearance.leaves

    #TODO is it relevant here?
    @property
    def temperature(self):
        #TODO modify update() to get Atmos object...
        return T

    @property
    def growing_temperature(self):
        return self.gst_tracker.rate

    @property
    def optimal_temperature(self):
        #TODO parmaterize?
        return 32.1

    @property
    def germinating(self):
        return self.germination.ing()

    @property
    def emerging(self):
        return self.emergence.ing()

    @property
    def dying(self):
        pass

    @property
    def gdd_after_emergence(self):
        if self.emergence.over():
            #HACK tracker is reset when emergence is over
            return self.gst_tracker.rate
        else:
            return 0
