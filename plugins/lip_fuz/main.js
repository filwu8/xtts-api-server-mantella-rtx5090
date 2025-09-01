"use strict"

const fs = require("fs")

let hasShownModal = false

const setupSettings = () => {
    const pathRoot = `${__dirname.replace(/\\/g,"/").replace("/javascript", "")}/`.replace("/resources/app/resources/app", "/resources/app")
    window.pluginsManager.registerINIFile("lip_fuz", "lip_fuz_settings", `${pathRoot}/lip_fuz.ini`)

    if (hasShownModal) {
        return
    }

    try {
        fs.statSync(`${path}/plugins/lip_fuz/FaceFXWrapper.exe`)
    } catch (e) {
        setTimeout(() => {
            window.errorModal(`The dependency file at the following location is not found, for the lip/fuz plugin:<br><br>${path}/plugins/lip_fuz/FaceFXWrapper.exe<br><br>Be sure to download this file from the Nexus page linked on the plugin page.`)
        }, 1000)
    }

    hasShownModal = true

    setTimeout(() => {
        if (window.userSettings.audio.hz!=44100 || window.userSettings.audio.bitdepth!="pcm_s16le" || window.userSettings.audio.format!="wav") {
            window.confirmModal(`The ffmpeg audio settings for lip_fuz need to be:<br>Hz: 44100 (Yours: ${window.userSettings.audio.hz})<br>Bit depth: pcm_s16le (Yours: ${window.userSettings.audio.bitdepth})<br>Format: .wav (Yours: .${window.userSettings.audio.format})<br><br>Change your settings to these?`).then(resp => {
                if (resp) {
                    window.userSettings.audio.hz = 44100
                    setting_audio_hz.value = 44100
                    window.userSettings.audio.bitdepth = "pcm_s16le"
                    setting_audio_bitdepth.value = "pcm_s16le"
                    window.userSettings.audio.format = "wav"
                    setting_audio_format.value = "wav"
                    window.saveUserSettings()
                }
            })
        }
    }, 1000)
}

const setup = () => {
    setupSettings()
}
const teardown = () => {
    document.querySelectorAll(".lip_fuz_plugin_setting").forEach(elem => elem.remove())
    hasShownModal = false
}
exports.setup = setup
exports.teardown = teardown
exports.setupSettings = setupSettings