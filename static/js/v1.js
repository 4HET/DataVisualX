// t='//www.dianping.com', e={shopId: 'H8mrf4qzTjyV6sji'}

h = function (t, e) {
    if (window.Rohr_Opt && window.Rohr_Opt.reload) {
        var i = window.Rohr_Opt
            , n = ""
            , o = e;
        "string" == typeof o && o.startsWith("_fb_=") && (o = "");
        var r = function (t) {
            var e = [];
            for (var i in t)
                e.push(i + "=" + t[i]);
            return e.join("&")
        }(o)
            , s = location.protocol + t + "?" + r;
        try {
            n = i.reload(s) || ""
        } catch (t) {
            console.log("获取token失败:" + t)
        }
        return n
    }
};

iP.reload = function (jv) {
    var jw;
    var jx = {};
    if (typeof jv === _$_543c[91]) {
        jx = iO.parse(jv.split(_$_543c[146])[1])
    } else {
        if (typeof jv === _$_543c[2]) {
            jx = jv
        }
    }
    ;iP.sign = iJ(jx);
    iP.cts = new Date().getTime();
    jw = iI(iP);
    if (Rohr_Opt.LogVal && typeof (window) !== _$_543c[0]) {
        window[Rohr_Opt.LogVal] = encodeURIComponent(jw)
    }
    ;
    return jw
}

b.exports = function (ir, it, im, de) {
    it = it || _$_543c[121];
    im = im || _$_543c[122];
    var dl = {};
    if (typeof ir !== _$_543c[91] || ir.length === 0) {
        return dl
    }
    ;var is = /\+/g;
    ir = ir.split(it);
    var iq = 1000;
    if (de && typeof de.maxKeys === _$_543c[98]) {
        iq = de.maxKeys
    }
    ;var ds = ir.length;
    if (iq > 0 && ds > iq) {
        ds = iq
    }
    ;
    for (var cs = 0; cs < ds; ++cs) {
        var iv = ir[cs].replace(is, _$_543c[123]), io = iv.indexOf(im), ip, iu, cr, hQ;
        if (io >= 0) {
            ip = iv.substr(0, io);
            iu = iv.substr(io + 1)
        } else {
            ip = iv;
            iu = _$_543c[60]
        }
        ;cr = decodeURIComponent(ip);
        hQ = decodeURIComponent(iu);
        if (!ik(dl, cr)) {
            dl[cr] = hQ
        } else {
            if (il(dl[cr])) {
                dl[cr].push(hQ)
            } else {
                dl[cr] = [dl[cr], hQ]
            }
        }
    }
    ;
    return dl
}

function ik(dl, ix) {
    return Object.prototype.hasOwnProperty.call(dl, ix)
}

var iJ = function (je) {
    var jd = [];
    var ck = Object.keys(je).sort();
    ck.forEach(function (jf, bx) {
        if (jf !== _$_543c[136] && jf !== _$_543c[137]) {
            jd.push(jf + _$_543c[122] + je[jf])
        }
    });
    jd = jd.join(_$_543c[121]);
    return iI(jd)
};

var iI = function (jc) {
    jc = cD.deflate(JSON.stringify(jc));
    jc = iD(jc);
    return jc
};

function cD(dd, de) {
    var dc = new cE(de);
    dc.push(dd, true);
    if (dc.err) {
        throw dc.msg || cH[dc.err]
    }
    ;
    return dc.result
}

function cE(de) {
    if (!(this instanceof cE)) {
        return new cE(de)
    }
    ;this.options = cK.assign({
        level: cL,
        method: cN,
        chunkSize: 16384,
        windowBits: 15,
        memLevel: 8,
        strategy: cM,
        to: _$_543c[60]
    }, de || {});
    var dg = this.options;
    if (dg.raw && (dg.windowBits > 0)) {
        dg.windowBits = -dg.windowBits
    } else {
        if (dg.gzip && (dg.windowBits > 0) && (dg.windowBits < 16)) {
            dg.windowBits += 16
        }
    }
    ;this.err = 0;
    this.msg = _$_543c[60];
    this.ended = false;
    this.chunks = [];
    this.strm = new cU();
    this.strm.avail_out = 0;
    var cZ = cT.deflateInit2(this.strm, dg.level, dg.method, dg.windowBits, dg.memLevel, dg.strategy);
    if (cZ !== cQ) {
        throw new Error(cH[cZ])
    }
    ;
    if (dg.header) {
        cT.deflateSetHeader(this.strm, dg.header)
    }
    ;
    if (dg.dictionary) {
        var df;
        if (typeof dg.dictionary === _$_543c[91]) {
            df = cI.string2buf(dg.dictionary)
        } else {
            if (cJ.call(dg.dictionary) === _$_543c[104]) {
                df = new Uint8Array(dg.dictionary)
            } else {
                df = dg.dictionary
            }
        }
        ;cZ = cT.deflateSetDictionary(this.strm, df);
        if (cZ !== cQ) {
            throw new Error(cH[cZ])
        }
        ;this._dict_set = true
    }
}

var iD = (function (cC) {
        var iH = [];
        var dY = 0;
        var bs = cC.length;
        var dG = 0;
        for (var cs = 0; cs < bs; ++cs) {
            dY += 1;
            if (dY === 3) {
                dY = 0
            }
            ;dG = iE(cC, cs);
            if (dY === 0) {
                iH.push(iF(((iE(cC, cs - 1) << 2) | (dG >> 6)) & 0x3F), iF(dG & 0x3F))
            } else {
                if (dY === 1) {
                    iH.push(iF((dG >> 2) & 0x3F))
                } else {
                    iH.push(iF(((iE(cC, cs - 1) << 4) | (dG >> 4)) & 0x3F))
                }
            }
            ;
            if (cs === bs - 1 && dY > 0) {
                iH.push(iF((dG << ((3 - dY) << 1)) & 0x3F))
            }
        }
        ;
        if (dY) {
            while (dY < 3) {
                dY += 1;
                iH.push(_$_543c[122])
            }
        }
        ;
        return iH.join(_$_543c[60])
    }
);
b.exports = iD


